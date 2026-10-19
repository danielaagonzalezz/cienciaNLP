"""Prueba de humo: el paquete se puede importar."""


def test_package_imports():
    import ciencianlp

    assert ciencianlp.__version__
    