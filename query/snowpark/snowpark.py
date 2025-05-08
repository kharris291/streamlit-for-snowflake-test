import utils

session = utils.get_connector()
query = """
    With q1 AS(
        select department, floor(avg(salary)) as avg_salary from employees
        group by department
        order by department
    )

    select e.department, e.employee_name, e.salary, (salary + (q1.avg_salary *0.1)) as new_sal
    from employees e
    join q1 on q1.department = e.department
    where job = 'MANAGER'
    order by e.department, e.employee_name;
"""
df = session.sql(query).to_pandas()
print(df)