from django.db import models
#모델 이름과 테이블 이름이 다르다는 것을 명심! 이거 안되면 MariaDB에 따로 모델을 만든다. 모델명을 제대로 써야 MariaDB의 DB에 제대로 접근할 수 있다.
#명령어: python manage.py inspectdb - 기존의 DB/모델을 장고 모델로 가져올 수 있다. 그리고 그 안의 Meta data까지 가져오므로 정확하게 modeling 가능


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BsPrd(models.Model):
    prd_cd = models.CharField(primary_key=True, max_length=5)
    year = models.IntegerField(db_column='YEAR')  # Field name made lowercase.
    turn = models.IntegerField()
    prd_str_dt = models.DateField()
    job_srv_str_dt = models.DateField(blank=True, null=True)
    job_srv_end_dt = models.DateField(blank=True, null=True)
    prd_end_dt = models.DateField(blank=True, null=True)
    prd_done_yn = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'bs_prd'


class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=20)
    leader = models.ForeignKey('Employee', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employee(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(db_column='NAME', max_length=30)  # Field name made lowercase.
    birth_date = models.DateField(blank=True, null=True)
    sex = models.JSONField(blank=True, null=True)
    position = models.CharField(db_column='POSITION', max_length=10, blank=True, null=True)  # Field name made lowercase.
    salary = models.IntegerField(blank=True, null=True)
    dept = models.ForeignKey(Department, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee'


class Mysite44JobDescriptionInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_name = models.CharField(max_length=20)
    department = models.CharField(max_length=20)
    team_name = models.CharField(max_length=20)
    manager = models.CharField(max_length=20)
    outline = models.CharField(max_length=100)
    responsibility = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'mysite44_job_description_info'


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(db_column='NAME', unique=True, max_length=20)  # Field name made lowercase.
    leader = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class Student(models.Model):
    studentid = models.AutoField(primary_key=True)
    studentname = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'student'


class Student2(models.Model):
    studentid = models.CharField(max_length=50)
    studentname = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'student2'


class WorksOn(models.Model):
    empl = models.OneToOneField(Employee, models.DO_NOTHING, primary_key=True)
    proj = models.ForeignKey(Project, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'works_on'
        unique_together = (('empl', 'proj'),)


class CcCdDetail(models.Model):
    domain_cd = models.OneToOneField('CcCdHeader', models.DO_NOTHING, db_column='domain_cd', primary_key=True)
    cc_code = models.CharField(max_length=2)
    cc_code_nm = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cc_cd_detail'
        unique_together = (('domain_cd', 'cc_code'),)


class CcCdHeader(models.Model):
    domain_cd = models.CharField(primary_key=True, max_length=2)
    domain_nm = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'cc_cd_header'


class BsAcnt(models.Model):
    dept_id = models.CharField(primary_key=True, max_length=5)
    prd_cd = models.ForeignKey('BsDept', models.DO_NOTHING, related_name='bs_acnt_prd_cd', db_column='prd_cd')
    dept_cd = models.ForeignKey('BsDept', models.DO_NOTHING, related_name='bs_acnt_dept_cd', db_column='dept_cd', to_field='dept_cd')

    class Meta:
        managed = False
        db_table = 'bs_acnt'
        unique_together = (('dept_id', 'prd_cd', 'dept_cd'),)


class BsDept(models.Model):
    prd_cd = models.OneToOneField('BsPrd', models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_cd = models.CharField(max_length=4, unique=True)
    dept_nm = models.CharField(max_length=50)
    dept_mgr_yn = models.CharField(max_length=1, blank=True, null=True)
    dept_to = models.IntegerField(blank=True, null=True)
    dept_po = models.IntegerField(blank=True, null=True)
    job_details_submit_yn = models.CharField(max_length=1, blank=True, null=True)
    job_details_submit_dttm = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bs_dept'
        unique_together = (('prd_cd', 'dept_cd'),)


class BsDeptGrp(models.Model):
    prd_cd = models.OneToOneField(BsDept, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_domain = models.ForeignKey('BsDeptGrpDomain', models.DO_NOTHING, related_name='BsDeptGrp_dept_domain', db_column='dept_domain', to_field='dept_domain')
    dept_grp_nm = models.ForeignKey('BsDeptGrpDomain', models.DO_NOTHING, related_name='BsDeptGrp_dept_grp_nm', db_column='dept_grp_nm', to_field='dept_grp_nm')
    dept_cd = models.ForeignKey(BsDept, models.DO_NOTHING, related_name='BsDeptGrp_dept_cd', db_column='dept_cd', to_field='dept_cd')

    class Meta:
        managed = False
        db_table = 'bs_dept_grp'
        unique_together = (('prd_cd', 'dept_domain', 'dept_grp_nm', 'dept_cd'),)


class BsDeptResp(models.Model):
    prd_cd = models.OneToOneField(BsDept, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_cd = models.ForeignKey(BsDept, models.DO_NOTHING, related_name='BsDeptResp_dept_cd', db_column='dept_cd', to_field='dept_cd')
    dept_resp_ordr = models.IntegerField()
    dept_resp = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'bs_dept_resp'
        unique_together = (('prd_cd', 'dept_cd', 'dept_resp_ordr'),)


class BsDeptGrpDomain(models.Model):
    prd_cd = models.OneToOneField('BsPrd', models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_domain = models.CharField(max_length=50, unique=True)
    dept_grp_nm = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = 'bs_dept_grp_domain'
        unique_together = (('prd_cd', 'dept_domain', 'dept_grp_nm'),)


class BsJob(models.Model):
    prd_cd = models.OneToOneField('BsPrd', models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    job_cd = models.CharField(max_length=5, unique=True)
    job_nm = models.CharField(max_length=50)
    job_type = models.CharField(max_length=4)
    job_descrp = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'bs_job'
        unique_together = (('prd_cd', 'job_cd'),)


class BsJobDept(models.Model):
    prd_cd = models.OneToOneField(BsJob, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_cd = models.ForeignKey(BsDept, models.DO_NOTHING, db_column='dept_cd', to_field='dept_cd')
    job_cd = models.ForeignKey(BsJob, models.DO_NOTHING, related_name='job_cd_jobdept', db_column='job_cd', to_field='job_cd')
    job_by = models.CharField(max_length=500)
    create_dttm = models.DateTimeField()
    alter_dttm = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bs_job_dept'
        unique_together = (('prd_cd', 'dept_cd', 'job_cd'),)


class BsJobResp(models.Model):
    prd_cd = models.OneToOneField(BsJob, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    job_cd = models.ForeignKey(BsJob, models.DO_NOTHING, related_name='job_cd_bsjobresp', db_column='job_cd', to_field='job_cd')
    job_resp_ordr = models.IntegerField()
    job_resp = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'bs_job_resp'
        unique_together = (('prd_cd', 'job_cd', 'job_resp_ordr'),)


class BsPosList(models.Model):
    prd_cd = models.OneToOneField('BsPrd', models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    pos_nm = models.CharField(max_length=10, unique=True)
    pos_ordr = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bs_pos_list'
        unique_together = (('prd_cd', 'pos_nm'),)


class BsPosGrade(models.Model):
    prd_cd = models.OneToOneField('BsWorkGrade', models.DO_NOTHING, related_name='BsPosGrade_prd_cd', db_column='prd_cd', primary_key=True)
    pos_nm = models.CharField(max_length=10)
    work_grade = models.ForeignKey('BsWorkGrade', models.DO_NOTHING, db_column='work_grade', to_field='work_grade')

    class Meta:
        managed = False
        db_table = 'bs_pos_grade'
        unique_together = (('prd_cd', 'work_grade', 'pos_nm'),)


class BsMbr(models.Model):
    prd_cd = models.OneToOneField('BsPosList', models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_cd = models.ForeignKey(BsDept, models.DO_NOTHING, db_column='dept_cd', to_field='dept_cd')
    mbr_nm = models.CharField(max_length=10, unique=True)
    pos_nm = models.CharField(max_length=10)
    ttl_nm = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'bs_mbr'
        unique_together = (('prd_cd', 'dept_cd', 'mbr_nm'),)


class BsMbrGrpNm(models.Model):
    prd_cd = models.OneToOneField(BsDept, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_cd = models.ForeignKey(BsDept, models.DO_NOTHING, related_name='BsMbrGrpNm_dept_cd', db_column='dept_cd', to_field='dept_cd')
    mbr_grp_nm = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = 'bs_mbr_grp_nm'
        unique_together = (('prd_cd', 'dept_cd', 'mbr_grp_nm'),)


class BsMbrGrp(models.Model):
    prd_cd = models.OneToOneField(BsMbr, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_cd = models.ForeignKey(BsDept, models.DO_NOTHING, related_name='BsMbrGrp_dept_cd', db_column='dept_cd', to_field='dept_cd')
    mbr_grp_nm = models.ForeignKey('BsMbrGrpNm', models.DO_NOTHING, db_column='mbr_grp_nm', to_field='mbr_grp_nm')
    mbr_nm = models.ForeignKey(BsMbr, models.DO_NOTHING, related_name='BsMbrGrp_mbr_nm', db_column='mbr_nm', to_field='mbr_nm')
    work_ratio = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bs_mbr_grp'
        unique_together = (('prd_cd', 'dept_cd', 'mbr_grp_nm', 'mbr_nm'),)


class BsStdWrkTm(models.Model):
    prd_cd = models.OneToOneField(BsPrd, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    total_dys = models.IntegerField()
    std_wrk_able_dys = models.IntegerField()
    std_wrk_tm_per_dy = models.IntegerField()
    spare_r = models.DecimalField(max_digits=2, decimal_places=1)
    std_wrk_able_tm = models.DecimalField(max_digits=5, decimal_places=1)
    ade_ot_tm = models.IntegerField()
    std_wrk_tm = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta:
        managed = False
        db_table = 'bs_std_wrk_tm'


class BsTtlCnt(models.Model):
    prd_cd = models.OneToOneField(BsDept, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_cd = models.ForeignKey(BsDept, models.DO_NOTHING, related_name='BsTtlCnt_dept_cd', db_column='dept_cd', to_field='dept_cd')
    ttl_nm = models.CharField(max_length=10)
    ttl_cnt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bs_ttl_cnt'
        unique_together = (('prd_cd', 'dept_cd', 'ttl_nm'),)


class BsTtlList(models.Model):
    prd_cd = models.OneToOneField(BsPrd, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    ttl_nm = models.CharField(max_length=10)
    ttl_ordr = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bs_ttl_list'
        unique_together = (('prd_cd', 'ttl_nm'),)


class BsWlOvSht(models.Model):
    prd_cd = models.OneToOneField(BsPrd, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    ov_sht_min = models.DecimalField(max_digits=2, decimal_places=1)
    ov_sht_max = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        managed = False
        db_table = 'bs_wl_ov_sht'


class BsWorkGrade(models.Model):
    prd_cd = models.OneToOneField(BsPrd, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    work_grade = models.CharField(max_length=2, unique=True)
    work_lv_min = models.IntegerField()
    work_lv_max = models.IntegerField()
    workload_wt = models.DecimalField(max_digits=4, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'bs_work_grade'
        unique_together = (('prd_cd', 'work_grade'),)


class MbrJobGrp(models.Model):
    prd_cd = models.CharField(unique=True, primary_key=True, max_length=5)
    dept_cd = models.CharField(unique=True, max_length=4)
    job_grp_nm = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'mbr_job_grp'
        unique_together = (('prd_cd', 'dept_cd', 'job_grp_nm'),)


class MbrJobGrpDetail(models.Model):
    prd_cd = models.OneToOneField(MbrJobGrp, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_cd = models.ForeignKey(MbrJobGrp, models.DO_NOTHING, related_name='MbrJobGrp_dept_cd', db_column='dept_cd', to_field='dept_cd')
    job_grp_nm = models.ForeignKey(MbrJobGrp, models.DO_NOTHING, related_name='MbrJobGrp_job_grp_nm', db_column='job_grp_nm', to_field='job_grp_nm')
    job_grp_mbr_nm = models.CharField(max_length=10)
    work_ratio = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'mbr_job_grp_detail'
        unique_together = (('prd_cd', 'dept_cd', 'job_grp_nm', 'job_grp_mbr_nm'),)


class JobActivity(models.Model):
    prd_cd = models.OneToOneField('JobTask', models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_cd = models.ForeignKey(BsDept, models.DO_NOTHING, related_name='BsDept_dept_cd_JA', db_column='dept_cd', to_field='dept_cd')
    job_cd = models.ForeignKey(BsJob, models.DO_NOTHING, related_name='BsJob_job_cd_JA', db_column='job_cd', to_field='job_cd')
    duty_nm = models.ForeignKey('JobTask', models.DO_NOTHING, related_name='JobTask_duty_nm_JA', db_column='duty_nm', to_field='duty_nm')
    task_nm = models.ForeignKey('JobTask', models.DO_NOTHING, related_name='JobTask_task_nm_JA', db_column='task_nm', to_field='task_nm')
    act_nm = models.CharField(max_length=300)
    act_prsn_chrg = models.CharField(max_length=100, blank=True, null=True)
    act_prfrm_freq = models.CharField(max_length=2)
    act_prfrm_cnt = models.IntegerField(blank=True, null=True)
    act_prfrm_cnt_ann = models.IntegerField(blank=True, null=True)
    act_prfrm_tm_cs = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    act_prfrm_tm_ann = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    dept_rltd = models.CharField(max_length=100, blank=True, null=True)
    final_rpt_to = models.CharField(max_length=50, blank=True, null=True)
    rpt_nm = models.CharField(max_length=100, blank=True, null=True)
    job_seq = models.IntegerField()
    duty_seq = models.IntegerField()
    task_seq = models.IntegerField()
    act_seq = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'job_activity'
        unique_together = (('prd_cd', 'dept_cd', 'job_cd', 'duty_nm', 'task_nm', 'act_nm'),)


class JobSpcfc(models.Model):
    prd_cd = models.OneToOneField(BsJob, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_cd = models.ForeignKey(BsDept, models.DO_NOTHING, related_name='BsDept_dept_cd_JSF', db_column='dept_cd', to_field='dept_cd')
    job_cd = models.ForeignKey(BsJob, models.DO_NOTHING, related_name='BsJob_job_cd_JSF', db_column='job_cd', to_field='job_cd')
    ctgry = models.CharField(max_length=100)
    ctgry_ordr = models.IntegerField()
    ctgry_cnts = models.CharField(max_length=300, blank=True, null=True)
    cc_cd_yn = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_spcfc'
        unique_together = (('prd_cd', 'dept_cd', 'job_cd', 'ctgry', 'ctgry_ordr'),)


class JobTask(models.Model):
    prd_cd = models.OneToOneField(BsWorkGrade, models.DO_NOTHING, db_column='prd_cd', primary_key=True)
    dept_cd = models.ForeignKey(BsDept, models.DO_NOTHING, related_name='BsDept_dept_cd_JT', db_column='dept_cd', to_field='dept_cd')
    job_cd = models.ForeignKey(BsJob, models.DO_NOTHING, related_name='BsJob_job_cd2', db_column='job_cd', to_field='job_cd')
    duty_nm = models.CharField(max_length=100, unique=True)
    task_nm = models.CharField(max_length=200, unique=True)
    task_prsn_chrg = models.CharField(max_length=500, blank=True, null=True)
    work_lv_imprt = models.IntegerField(blank=True, null=True)
    work_lv_dfclt = models.IntegerField(blank=True, null=True)
    work_lv_prfcn = models.IntegerField(blank=True, null=True)
    work_lv_sum = models.IntegerField(blank=True, null=True)
    work_grade = models.ForeignKey(BsWorkGrade, models.DO_NOTHING, related_name='BsWorkGrade_work_grade_JT', db_column='work_grade', to_field='work_grade', blank=True, null=True)
    work_attrbt = models.CharField(max_length=3, blank=True, null=True)
    prfrm_tm_ann = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    job_seq = models.IntegerField()
    duty_seq = models.IntegerField()
    task_seq = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'job_task'
        unique_together = (('prd_cd', 'dept_cd', 'job_cd', 'duty_nm', 'task_nm'),)