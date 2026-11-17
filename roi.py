# Задание 2: расчёт ROI системы мониторинга трафика (в долларах)

# Данные из отчёта IBM / Ponemon Institute "Cost of a Data Breach 2025":
# средняя стоимость инцидента в мире 4,44 млн $
# https://www.ibm.com/think/x-force/2025-cost-of-a-data-breach-navigating-ai
incident_cost = 4_440_000

# Остальное - допущения для учебного кейса, не реальные данные
system_cost = 60_000 + 3 * 40_000    # покупка + поддержка за 3 года
incidents_per_year = 0.15            # вероятность серьёзного инцидента в год
loss_reduction = 0.30                # на сколько система снижает ущерб
downtime_hours = 20                  # часов простоя в год
downtime_hour_cost = 8_000           # стоимость часа простоя
downtime_reduction = 0.40            # на сколько сокращается простой
leak_losses = 150_000                # потери от утечек в год
leak_reduction = 0.35                # на сколько сокращаются потери


def calculate_roi():
    years = 3
    saved_incidents = incident_cost * incidents_per_year * loss_reduction
    saved_downtime = downtime_hours * downtime_hour_cost * downtime_reduction
    saved_leaks = leak_losses * leak_reduction
    benefit = (saved_incidents + saved_downtime + saved_leaks) * years
    roi = (benefit - system_cost) / system_cost * 100

    print(f"Экономия на инцидентах в год: {saved_incidents:,.0f} $")
    print(f"Экономия на простое в год: {saved_downtime:,.0f} $")
    print(f"Экономия на утечках в год: {saved_leaks:,.0f} $")
    print(f"За 3 года выгода {benefit:,.0f} $, затраты {system_cost:,.0f} $")
    print(f"ROI = (выгода - затраты) / затраты = {roi:.0f}%")
    return roi
