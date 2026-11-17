# Задание 3: интеграции с внешними системами.
# Это заглушки: данные ненастоящие, реальные ключи в код не пишем.
# В реальной системе вместо списков были бы запросы к API.
from alerts import send_alert
from audit import log


def get_biometric_sessions():
    """Биометрическая аутентификация: входы в систему и точность распознавания"""
    return [
        {"user": "admin", "score": 0.97},
        {"user": "analyst", "score": 0.82},
    ]


def get_cloud_logs(provider):
    """Логи трафика из облака (AWS VPC Flow Logs или Azure NSG Flow Logs)"""
    return [
        {"destination_ip": "198.51.100.7", "provider": provider},
        {"destination_ip": "203.0.113.50", "provider": provider},
    ]


def get_threat_ips(source):
    """Базы угроз: списки плохих IP из MISP и AlienVault OTX"""
    if source == "misp":
        return ["198.51.100.7"]
    return ["203.0.113.50"]


def run_integrations():
    # 1. слабые биометрические входы
    for s in get_biometric_sessions():
        if s["score"] < 0.9:
            text = f"слабая биометрия у {s['user']}: {s['score']}"
            log("WEAK_BIOMETRIC", text)
            send_alert(text)

    # 2. логи облаков сверяем с базами угроз
    cloud_logs = get_cloud_logs("aws") + get_cloud_logs("azure")
    for source in ["misp", "otx"]:
        bad_ips = get_threat_ips(source)
        for row in cloud_logs:
            if row["destination_ip"] in bad_ips:
                text = (f"{row['provider']}: обращение к IP "
                        f"{row['destination_ip']} из базы {source}")
                log("THREAT_MATCH", text)
                send_alert(text)
