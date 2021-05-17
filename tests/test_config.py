import pytest


def test_make_empty_conf():
    root = test_make_tree()
    conf = ConfigBase(root)
    return conf


def test_conf_type():
    conf = test_make_empty_conf()

    with pytest.raises(ValueError):
        conf['linear_solver.iterative.gmres.restart'] = 'toto'


def test_conf_script():
    conf = test_make_empty_conf()

    conf['verbose'] = True
    conf["linear_solver.direct.cholesky"] = True
    conf['linear_solver.iterative.bicgstab'] = True
    conf['linear_solver.iterative.gmres.restart'] = 10
    conf['linear_solver.iterative.gmres'] = True

    assert conf['verbose'] == True
    assert conf['linear_solver.iterative.gmres.restart'] == 10
    assert conf['linear_solver.iterative.gmres'] == True
    assert conf['linear_solver.iterative.maxit'] == 100
    assert conf['newton.maxit'] == 30

    return conf


def test_conf_cli():
    conf = test_conf_script()
    conf.load_cli([
        "--linear_solver.iterative.tolerance", "1e-4",
        "--verbose", "False",
        "--linear_solver.iterative.gmres.restart", "20"
    ])

    assert conf['verbose'] == False
    assert conf['linear_solver.iterative.gmres.restart'] == 20
    assert conf['linear_solver.iterative.gmres'] == True
    assert conf['linear_solver.iterative.maxit'] == 100
    assert conf['linear_solver.iterative.tolerance'] == 1e-4
    assert conf['newton.maxit'] == 30


def test_conf_cli_alone():
    conf = test_make_empty_conf()

    conf.load_cli([
        '--verbose', 'True',
        "--linear_solver.direct.cholesky", 'True',
        '--linear_solver.iterative.bicgstab', 'True',
        '--linear_solver.iterative.gmres.restart', '10',
        '--linear_solver.iterative.gmres', 'True',
    ])

    assert conf['verbose'] == True
    assert conf['linear_solver.iterative.gmres.restart'] == 10
    assert conf['linear_solver.iterative.gmres'] == True
    assert conf['linear_solver.iterative.maxit'] == 100
    assert conf['newton.maxit'] == 30
