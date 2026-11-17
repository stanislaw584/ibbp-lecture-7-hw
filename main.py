from analyzer import NetworkTrafficAnalyzer
from integrations import run_integrations
from roi import calculate_roi

print("=== Задание 1: DDoS, журнал аудита, оповещения ===")
analyzer = NetworkTrafficAnalyzer("ТехноПрофи")
analyzer.simulate_traffic(with_ddos=True)
analyzer.detect_blocked_ports()
analyzer.detect_ddos()

print("\n=== Задание 2: ROI ===")
calculate_roi()

print("\n=== Задание 3: интеграции ===")
run_integrations()
