SQL_GET_USER_COMPANIES = '''
select c.ID, c.NAME, c.ARCHIVED
  from company c,
       rules r
 where 1=1
   and r.COMPANY_ID = c.ID
   and USER_ID = :user_id
   and r.ROLE = IFNULL(:user_role,r.ROLE)
'''

SQL_GET_USER_BRANDS = '''
select b.ID, b.NAME, b.COMPANY_ID, b.ARCHIVED
  from company c,
       brand b,
       rules r
 where 1=1
   and r.COMPANY_ID = c.ID
   and USER_ID = :user_id
   and r.ROLE = IFNULL(:user_role,r.ROLE)
   and b.COMPANY_ID = c.ID
UNION ALL
select b.ID, b.NAME, b.COMPANY_ID, b.ARCHIVED
  from brand b,
       rules r
 where 1=1
   and b.ID = r.BRAND_ID
   and USER_ID = :user_id
   and r.ROLE = IFNULL(:user_role,r.ROLE)
'''


SQL_GET_USER_TEMPLATES = '''
select t.ID, t.NAME, t.BRAND_ID, t.PATH
  from company c,
       brand b,
       template t,
       rules r
 where 1=1
   and r.COMPANY_ID = c.ID
   and USER_ID = :user_id
   and r.ROLE = IFNULL(:user_role,r.ROLE)
   and b.COMPANY_ID = c.ID
   and t.BRAND_ID = b.ID
UNION ALL
select t.ID, t.NAME, t.BRAND_ID, t.PATH
  from brand b,
       template t,
       rules r
 where 1=1
   and b.ID = r.BRAND_ID
   and USER_ID = :user_id
   and r.ROLE = IFNULL(:user_role,r.ROLE)
   and t.BRAND_ID = b.ID
UNION ALL
select t.ID, t.NAME, t.BRAND_ID, t.PATH
  from template t,
       rules r
 where 1=1
   and t.ID = r.TEMPLATE_ID
   and USER_ID = :user_id
   and r.ROLE = IFNULL(:user_role,r.ROLE)

'''