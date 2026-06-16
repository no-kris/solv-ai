import json
import subprocess

from docker.client import DockerClient

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

    def build_image(self):
        """
        Reads the dockerfile contained in the docker directory and builds the docker image.
        """
        self.client.images.build(path="./docker", tag=self.image_name)

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
                [json.dumps([t.model_dump() for t in tests]), json.dumps(param_names)],
                input=code.encode(),
                timeout=5,  # 5 second timeout
                mem_limit="128m",  # Max 128MB
                cpus=0.5,  # Max 50% CPU
                remove=True,  # Auto-cleanup
            )

            test_results = json.loads(result)
            return ValidationResponse(
                passed=test_results["passed"], total=test_results["total"]
            )
        except subprocess.TimeoutExpired:
            return CustomResponse(
                success=False, error="Code execution timed out (infinite loop?)"
            )
        except Exception as e:
            return CustomResponse(success=False, error=f"Execution error: {str(e)}")


executor = DockerExecutor()
