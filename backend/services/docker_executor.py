import json
import subprocess

from docker.client import DockerClient
from docker.errors import ImageNotFound

import docker
from schemas.schemas import (
    CustomResponse,
    GenericTestCase,
    GraphTestCase,
    LinkedListTestCase,
    TreeTestCase,
    ValidationResponse,
)


class DockerExecutor:
    def __init__(self, image_name: str = "solv-ai-code-executor"):
        """
        Connect to the docker daemon and start a docker image.
        """
        self.client: DockerClient = docker.DockerClient()
        self.image_name: str = image_name

    def image_exists(self) -> bool:
        """Check if image already exists."""
        try:
            self.client.images.get(self.image_name)
            return True
        except ImageNotFound:
            return False

    def build_image(self):
        """Build image only if it doesn't exist."""
        if self.image_exists():
            print(f"Image {self.image_name} already exists, skipping build")
            return

        self.client.images.build(
            path=".", dockerfile="docker/dockerfile", tag=self.image_name
        )

    def execute(
        self,
        code: str,
        tests: list[
            GenericTestCase | TreeTestCase | LinkedListTestCase | GraphTestCase
        ],
        param_names: list[str],
    ) -> ValidationResponse | CustomResponse:
        """Execute code in a container and return results."""
        try:
            result = self.client.containers.run(
                self.image_name,
                command=[
                    "python",
                    "execute.py",
                    json.dumps([t.model_dump() for t in tests]),
                    json.dumps(param_names),
                    code,
                ],
                mem_limit="128m",
                cpu_quota=50000,
                cpu_period=100000,
                remove=True,
            )
            output = json.loads(result)
            if not output.get("success", False):
                return output
            return ValidationResponse(passed=output["passed"], total=len(tests))
        except subprocess.TimeoutExpired:
            return CustomResponse(
                success=False, error="Code execution timed out (infinite loop?)"
            )
        except Exception as e:
            return CustomResponse(success=False, error=f"Execution error: {str(e)}")


executor = DockerExecutor()
executor.build_image()
