import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """测试/health端点是否正常返回"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert data["service"] == "day08-flask-upgrade"


def test_metrics_api_with_login(client):
    """测试/api/metrics端点（登录后）"""
    with client.session_transaction() as sess:
        sess["username"] = "student"
    
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert "metrics" in data
    assert len(data["metrics"]) == 4
    for metric in data["metrics"]:
        assert "label" in metric
        assert "value" in metric
        assert "note" in metric


def test_categories_api_with_login(client):
    """测试/api/categories端点（登录后）"""
    with client.session_transaction() as sess:
        sess["username"] = "student"
    
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert data["category"] == "全部"
    assert "rows" in data


def test_categories_api_with_filter(client):
    """测试/api/categories端点带筛选参数"""
    with client.session_transaction() as sess:
        sess["username"] = "student"
    
    response = client.get("/api/categories?category=Fashion")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert data["category"] == "Fashion"
    assert "rows" in data


def test_metrics_api_without_login(client):
    """测试/api/metrics端点（未登录）"""
    response = client.get("/api/metrics")
    assert response.status_code == 302
    assert "/login" in response.location


def test_categories_api_without_login(client):
    """测试/api/categories端点（未登录）"""
    response = client.get("/api/categories")
    assert response.status_code == 302
    assert "/login" in response.location


def test_ask_api_empty_question(client):
    """测试/api/ask端点空问题返回400错误"""
    with client.session_transaction() as sess:
        sess["username"] = "student"
    
    response = client.post("/api/ask", json={"question": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert data["ok"] is False
    assert "error" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])