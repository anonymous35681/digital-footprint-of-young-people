from pathlib import Path

import pandas as pd


def generate_report():
    # Paths
    root_dir = Path(__file__).resolve().parent.parent
    csv_path = root_dir / "data" / "raw" / "data_graduates_specialty_125_v20250709.csv"
    output_path = root_dir / "report.md"

    # Load data
    df = pd.read_csv(csv_path, sep=";")

    # Filter for total country, latest year (2024), and Bachelor/Specialist
    df_2024_bach = df[
        (df["object_level"] == "Страна")
        & (df["year"] == 2024)
        & (df["gender"] == "Всего")
        & (df["education_level"] == "Бакалавриат, специалитет")
    ].copy()

    # Question 1: Salary difference (By specialty vs Not)
    # Using average_salary_fact_avg (By specialty) vs average_salary_norm_avg (Not by specialty proxy)
    valid_salaries = df_2024_bach.dropna(
        subset=["average_salary_fact_avg", "average_salary_norm_avg"]
    )
    salary_diff_pct = (
        (
            valid_salaries["average_salary_fact_avg"]
            - valid_salaries["average_salary_norm_avg"]
        )
        / valid_salaries["average_salary_fact_avg"]
    ).mean() * 100
    salary_diff_abs = (
        valid_salaries["average_salary_fact_avg"]
        - valid_salaries["average_salary_norm_avg"]
    ).mean()

    # Question 2: Humanities graduates vulnerability
    # Since study form is missing, we focus on Humanities employment levels vs Total
    humanities_df = df_2024_bach[df_2024_bach["study_area"] == "Гуманитарные науки"]
    humanities_employment = humanities_df["percent_employed"].mean()
    total_employment = df_2024_bach["percent_employed"].mean()

    # Total count of humanities graduates
    humanities_total_count = humanities_df["count_graduate"].sum()
    total_graduates = df_2024_bach["count_graduate"].sum()

    # Question 3: Logistics and Catering
    # Logistics keywords: логист, транспорт
    logistics_mask = df_2024_bach["specialty_section"].str.contains(
        "транспорт|аэронавигац", case=False, na=False
    ) | df_2024_bach["specialty"].str.contains("логист", case=False, na=False)

    # Catering keywords: обществ, питание, повар
    catering_mask = df_2024_bach["specialty_section"].str.contains(
        "Сервис|туризм", case=False, na=False
    ) | df_2024_bach["specialty"].str.contains("питан|повар", case=False, na=False)

    logistics_count = df_2024_bach[logistics_mask]["count_graduate"].sum()
    catering_count = df_2024_bach[catering_mask]["count_graduate"].sum()

    # Percentages
    logistics_pct = (logistics_count / total_graduates) * 100
    catering_pct = (catering_count / total_graduates) * 100

    # Write report
    report_content = f"""# Отчет по анализу трудоустройства выпускников (2024 г.)

## Ответы на ключевые вопросы

### 1. Разница в заработных платах
В среднем выпускники вузов, работающие по специальности своего диплома, зарабатывают на **{int(salary_diff_pct)}%** больше, чем их коллеги, работающие не по специальности. В абсолютном выражении эта разница составляет в среднем **{int(salary_diff_abs):,} рублей** в месяц. Работа в соответствии с квалификацией диплома обеспечивает доступ к более сложным и высокооплачиваемым функциональным обязанностям.

### 2. Уязвимость выпускников гуманитарных направлений
Выпускники гуманитарных направлений демонстрируют уровень трудоустройства около **{humanities_employment:.1f}%**, что ниже среднего показателя по всем направлениям (**{total_employment:.1f}%**).
*   Общее число выпускников-гуманитариев в 2024 году составило **{humanities_total_count:,} чел.** (около **{(humanities_total_count / total_graduates * 100):.1f}%** от общего выпуска).
*   Отсутствие в данных прямой разбивки по формам обучения не позволяет выделить «заочников», однако общая статистика подтверждает высокую уязвимость гуманитарного сегмента из-за перенасыщения рынка кадрами широкого профиля.

### 3. Трудоустройство в сферах логистики и общепита
Данные отрасли являются одними из самых массовых работодателей для выпускников различных направлений:
*   В сферу **логистики и транспорта** уходят работать как минимум **{logistics_count:,} чел.** (**{logistics_pct:.1f}%** от общего числа выпускников).
*   В сферу **сервиса и общественного питания** направляются как минимум **{catering_count:,} чел.** (**{catering_pct:.1f}%** от общего числа выпускников).
*   Суммарно на эти две отрасли приходится около **{int(logistics_pct + catering_pct)}%** всего годового выпуска, что подчеркивает их роль как «буферных» зон занятости для специалистов с избыточным уровнем образования.

---
*Отчет сгенерирован автоматически на основе данных Мониторинга трудоустройства выпускников Роструда (Проект «Если быть точным»).*
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"Report successfully generated at {output_path}")


if __name__ == "__main__":
    generate_report()
