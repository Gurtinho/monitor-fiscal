def test_status_jira():
    from services.status_jira import status_jira
    result = status_jira()
    assert result == "Estou operacional e pronto para ajudar! 🚀"