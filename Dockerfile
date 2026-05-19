FROM public.ecr.aws/lambda/python:3.12 AS builder

# =========================================================
# Dependencias del sistema necesarias para:
# - numpy
# - opencv
# - pdf2image
# - compilación de wheels
# =========================================================

RUN dnf update -y && \
    dnf install -y \
        gcc \
        gcc-c++ \
        make \
        cmake \
        tar \
        gzip \
        unzip \
        findutils \
        libffi-devel \
        openssl-devel \
        glib2 \
        mesa-libGL \
        poppler-utils && \
    dnf clean all

WORKDIR /build

COPY requirements.txt .

# =========================================================
# Instalar dependencias Python en /opt/python
# (ubicación estándar Lambda Layers/runtime)
# =========================================================

RUN pip install --upgrade pip setuptools wheel

RUN pip install \
    --no-cache-dir \
    -r requirements.txt \
    -t /opt/python

# =========================================================
# Runtime final
# =========================================================

FROM public.ecr.aws/lambda/python:3.12

# =========================================================
# SOLO librerías runtime necesarias
# =========================================================

RUN dnf update -y && \
    dnf install -y \
        glib2 \
        mesa-libGL \
        poppler-utils && \
    dnf clean all

# =========================================================
# Variables importantes
# =========================================================

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Opcional pero recomendado para OpenCV
ENV OPENCV_IO_ENABLE_OPENEXR=1

# =========================================================
# Copiar dependencias instaladas
# =========================================================

COPY --from=builder /opt/python /opt/python

# =========================================================
# Copiar app
# =========================================================

COPY app ${LAMBDA_TASK_ROOT}/app
COPY templates ${LAMBDA_TASK_ROOT}/templates

WORKDIR ${LAMBDA_TASK_ROOT}

# =========================================================
# Handler Lambda
# =========================================================

CMD ["app.main.handler"]