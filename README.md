# NCAP Exit Preview - Harness lab

A small stateless FastAPI service extracting only basic_exit_prices from
jngocorai/ncap-prod app/planner.py, source blob
ade68b5a9c626e402fa3f8670c4b7a654cd533ac.
The original percentage-based calculations are preserved.
Input validation and HTTP endpoints are added for this lab.
No database, broker, executor, account data, or credentials are needed.
This is a demonstration placeholder, not a production trading risk model.

## Understand the files
- app/planner.py: original NCAP calculation.
- app/main.py: validates inputs and exposes health, version, and preview endpoints.
- tests/test_api.py: API and calculation checks.
- Dockerfile: packages the service as a non-root container.
- k8s/: desired application Deployment and internal Service.

## Run and test
Use Python 3.12.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-test.txt
mkdir -p reports
python -m unittest discover -s tests -v
uvicorn app.main:app --port 8080
```
Open http://localhost:8080/docs to submit a preview request.
Example payload: {"direction":"LONG","signal_price":100}.
Expected stop: 99.7; targets: 100.6 and 101.

## Container
```bash
docker build --build-arg APP_VERSION=1.0.0 -t ncap-demo:1.0.0 .
docker run --rm -p 8080:8080 ncap-demo:1.0.0
```
APP_VERSION is baked into the image; use a unique version/tag for each CI build.
The Mac cluster is ARM64. CI must publish an ARM64 image or a multi-platform
image containing linux/arm64; a default AMD64-only image will not run natively.

## Harness CD
Configure a Kubernetes service with a DockerHub artifact and manifests from k8s/.
Harness resolves <+artifact.image> at deployment time; these manifests are not
ready for direct kubectl apply before that expression is replaced.
Use connector localk8s and a dedicated namespace such as ncap-demo.
Use standard Kubernetes CD with Harness canary orchestration, not GitOps.
The manifests describe the base workload; Harness manages canary creation,
cleanup, and promotion. Configure rollback and validation in the CD stage.
Replica-based canaries do not guarantee an exact percentage of HTTP traffic.

## Playback evidence
Record tests, image tag, successful CI run, canary and stable pods, validation,
promotion, and a controlled rollback exercise. Describe observations accurately.

