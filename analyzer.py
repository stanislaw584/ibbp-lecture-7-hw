# Упрощённый анализатор трафика из лекции 7 + расширения из задания 1
import random
from datetime import datetime, timedelta

import pandas as pd

from alerts import send_alert
from audit import log

BLOCKED_PORTS = [21, 23, 3389]   # запрещённые порты
PPS_LIMIT = 300                  # порог пакетов в секунду для DDoS


class NetworkTrafficAnalyzer:
    def __init__(self, company_name):
        self.company_name = company_name
        self.traffic = pd.DataFrame()
        self.violations = []

    def simulate_traffic(self, records=10000, with_ddos=False):
        """Генерируем случайный трафик за сутки, при желании добавляем DDoS"""
        random.seed(42)
        start = datetime(2026, 11, 16, 0, 0)
        ports = [443, 80, 53, 3389, 21, 25, 22]
        rows = []
        for _ in range(records):
            rows.append({
                "timestamp": start + timedelta(seconds=random.randint(0, 86399)),
                "source_ip": f"192.168.1.{random.randint(1, 50)}",
                "destination_ip": f"192.168.1.{random.randint(1, 50)}",
                "port": random.choice(ports),
            })
        if with_ddos:
            # атака: 800 пакетов в секунду в течение минуты на один адрес
            attack_start = start + timedelta(hours=10)
            for sec in range(60):
                for _ in range(800):
                    rows.append({
                        "timestamp": attack_start + timedelta(seconds=sec),
                        "source_ip": f"203.0.{random.randint(0, 255)}.{random.randint(1, 255)}",
                        "destination_ip": "192.168.1.5",
                        "port": 80,
                    })
        self.traffic = pd.DataFrame(rows)
        log("START", f"сгенерировано {len(self.traffic)} записей трафика")

    def report(self, kind, details):
        """Нарушение попадает в список, журнал аудита и оповещения"""
        self.violations.append({"type": kind, "details": details})
        log(kind, details)
        send_alert(f"[{self.company_name}] {kind}: {details}")

    def detect_blocked_ports(self):
        """Проверка запрещённых портов (как в лекции)"""
        bad = self.traffic[self.traffic["port"].isin(BLOCKED_PORTS)]
        if len(bad) > 0:
            self.report("BLOCKED_PORT", f"{len(bad)} событий на запрещённых портах")

    def detect_ddos(self):
        """Считаем пакеты в секунду на каждый адрес назначения.
        Если больше порога - это похоже на DDoS"""
        self.traffic["second"] = self.traffic["timestamp"].dt.floor("s")
        pps = self.traffic.groupby(["destination_ip", "second"]).size()
        attacks = pps[pps > PPS_LIMIT]
        for ip in attacks.index.get_level_values(0).unique():
            peak = attacks[ip].max()
            self.report("DDOS", f"адрес {ip}: пик {peak} пакетов в секунду")
