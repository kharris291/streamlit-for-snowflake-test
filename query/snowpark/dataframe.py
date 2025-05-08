from snowflake.snowpark.functions import call_function, col

import _utils

session = _utils.get_connector()

avg_sales = (session
             .table("EMPLOYEES")
             .select("DEPARTMENT", "SALARY")
             .group_by("DEPARTMENT")
             .agg({"SALARY": "AVG"})
             .select(
    "DEPARTMENT",
    call_function("FLOOR", col("AVG(SALARY)"))
    .alias("AVG_SALARY")
)
             .sort("DEPARTMENT")
             )
# avg_sales.show()

managers = (session.table("EMPLOYEES")
            .select("DEPARTMENT", "EMPLOYEE_NAME", "SALARY")
            .filter(col("JOB") == "MANAGER")
            .sort("DEPARTMENT", "EMPLOYEE_NAME")
            )

print(managers.collect())
(managers.join(avg_sales, managers.department == avg_sales.department)
 .select(
    managers.department.alias("DEPARTMENT"),
    managers.employee_name.alias("MANAGER"),
    managers.salary.alias("SALARY"),
    (managers.salary + (0.1 * col("AVG_SALARY"))).alias("DIFFERENCE"),
)
    .show()
 )
