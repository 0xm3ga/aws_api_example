# AWS API Example

Welcome to my `aws_api_example` repository! This is where I showcase my approach to API creation, focusing on robustness, thoroughness, and adherence to industry standards. I've designed it to serve as a practical demonstration of my coding philosophy, prioritizing scalability, cost-effectiveness, and a high degree of professionalism.

## My Approach

1. **Comprehensive Documentation**: I stick to OpenAPI 3.0 standards to ensure that my API documentation is thorough and up-to-date. Furthermore, I integrate Swagger UI to provide a user-friendly, interactive documentation interface, enhancing understandability and ease-of-use of the API.

2. **Modular, Production-Ready Code**: I design my code to be both modular and production-ready, making it robust, reusable, and simple to maintain. This allows for easy updates and readiness for production deployment.

3. **In-Depth Testing**: I employ a comprehensive suite of both unit and integration tests to ensure the reliability of my codebase. My testing protocols ensure that individual components function as expected, and that their interactions are well coordinated.

4. **Scalable and Cost-Effective Server Infrastructure**: I utilize Infrastructure-as-Code (IaC) principles in designing my server infrastructure, balancing scalability with cost-effectiveness. The result is a server set-up that is repeatable, scalable, and efficient in terms of resource utilization.

5. **Microservices Architecture**: I make use of a microservices architecture to ensure that each module in my codebase is independent, easy to update, and deployable separately. This provides my code with the flexibility and scalability necessary for modern application development.

## How to Get Started

Before diving in, you might want to familiarize yourself with the general structure of the project. I've arranged the repository for easy navigation, whether you're looking to explore the code, consult the documentation, or run tests.

I welcome any feedback or contributions you might have. If you spot something that could be improved or have any questions, feel free to submit an issue or a pull request. I'm always looking to improve and learn. Enjoy exploring my code!

## Code Quality

### Setting Up Pre-commit Hooks

To ensure code quality, run tests, and check for issues before each commit, I use pre-commit to manage pre-commit hooks.

Here's how to install and set up the pre-commit hooks:

### Install pre-commit

You can install pre-commit with pip:

```bash
pip install pre-commit
```

Pre-commit hooks are configured in the `.pre-commit-config.yaml` file in the root of the repository. The following hooks are included:

1. Black: A code formatter for Python.
2. Flake8: A Python tool that glues together pep8, PyFlakes, and Ned Batchelder’s McCabe script.
3. isort: A Python utility to sort imports.
4. mypy: An optional static type checker for Python.
5. Pytest: Runs tests using pytest.

### Install the git hook scripts

Run this command to install the git hook scripts:

```bash
pre-commit install
```

Now, when new changes are committed, the pre-commit hooks will automatically format the code and check for issues.

## Testing

Make sure to run this command to add project root into PYTHONPATH to simplify module import.

```bash
export PYTHONPATH="$PYTHONPATH:$(pwd)"
```

When writing tests I focus on normal cases, error cases, and edge cases to create a well-rounded set of tests for the lambda functions.
