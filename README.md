# AWS API Example

Welcome to the `aws_api_example` repository! This repository serves as a showcase for my approach to API creation, with a keen focus on robustness, thoroughness, and adherence to industry standards. It stands as a practical demonstration of my coding philosophy, where scalability, cost-effectiveness, and superior code quality take center stage.

## My Approach

1. **Scalable and Cost-Effective Server Infrastructure**: I employ Infrastructure-as-Code (IaC) principles when designing the server infrastructure, striking a balance between scalability and cost-effectiveness. The resulting server setup is repeatable, scalable, and resource-efficient.

2. **Microservices Architecture**: I ensure each module in the codebase remains independent and easy to update, test, and deploy separately. This is achieved by the thoughtful segregation of features and infrastructure into separate AWS SAM templates. These templates are nested together for efficient, seamless deployment.

3. **Comprehensive Testing**: My codebase is fortified by a comprehensive suite of both unit and integration (local and smoke) tests. This approach confirms that individual components function as expected, and their interactions are well-coordinated.

4. **Comprehensive Documentation**: I adhere to OpenAPI 3.0 standards for thorough and up-to-date API documentation. Additionally, I integrate Swagger Hosted UI to provide a user-friendly, interactive documentation interface, enhancing API understandability and usability.

## How to Get Started

Before diving in, you might want to familiarize yourself with the general structure of the project. I've arranged the repository for easy navigation, whether you're looking to explore the code, consult the documentation, or run tests.

## AWS Infrastructure

This example project breaks down the infrastructure into two microservices:

1. **API** (supporting different versions for a future-proof project structure). The API follows OpenAPI 3.0.1 standards.
2. **Docs** - An S3-hosted static website serving API documentation. It employs Swagger Hosted UI to automate documentation generation.

The infrastructure is orchestrated using nested AWS SAM templates, defining the infrastructure in its entirety. This infrastructure-as-code approach streamlines the creation (and eventual destruction) of the required AWS infrastructure with two straightforward commands: `sam build` and `sam deploy`. It's notably designed for a pipeline that accommodates multiple environments, adhering to AWS SAM best practices.

## CI/CD (using GitHub Actions)

- **Upload API docs** (`upload_docs`): This action updates the API documentation hosted in the `docs` subdomain.
- **Local integration tests** (`local_integration_tests`): This action initiates `sam local start-api` and tests all endpoints, ensuring the code functions correctly before deployment.

## Code Quality: Setting Up Pre-commit Hooks

This project uses `pre-commit` to ensure high code quality. This framework manages pre-commit hooks that run tests and check for issues before each commit, catching potential issues early.

### Installation and Setup

1. **Install pre-commit**: This can be achieved using pip, as shown below:

   ```bash
   pip install pre-commit
   ```

2. **Configure pre-commit hooks**: The configuration for pre-commit hooks is stored in the `.pre-commit-config.yaml` file, located in the root of the repository. The hooks included in this project are:

   - **Black**: A Python code formatter.
   - **Flake8**: A Python tool that bundles pep8, PyFlakes, and Ned Batchelder’s McCabe script for code linting.
   - **isort**: A utility to sort Python imports.
   - **mypy**: An optional static type checker for Python.
   - **Pytest**: Runs tests using the pytest framework.

3. **Install git hook scripts**: The following command installs the git hook scripts:

   ```bash
   pre-commit install
   ```

Upon successful installation, these pre-commit hooks will automatically format the code and check for issues each time a new commit is made, ensuring code quality and consistency throughout the development process.

## Testing

This project implements a two-fold testing approach: unit testing and integration testing, all facilitated by `pytest`.

- **Unit Testing**: These tests are responsible for verifying the correctness of individual code units, such as functions or methods.
- **Integration Testing**: This project conducts two types of integration tests:
  1. **Local Integration Tests**: Performed on the locally hosted API, these tests aim to catch and rectify any issues before code deployment.
  2. **Deployment Integration Tests**: Run post-deployment, these tests ensure the deployed code operates as expected in the production environment.

Before running the tests, it's crucial to add the project's root directory to the `PYTHONPATH`. This simplifies the module import process. You can do this with the following command:

```bash
export PYTHONPATH="$PYTHONPATH:$(pwd)"
```

Test cases are carefully designed to cover normal, error, and edge cases. This thorough approach ensures a well-rounded test suite for the lambda functions.

## Contributions and Feedback

Your feedback and contributions are always appreciated. If you notice areas for improvement, have any queries, or wish to contribute, feel free to submit an issue or a pull request. Continuous learning and improvement are core to this project. Enjoy exploring the code!
