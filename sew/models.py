from django.db import models

# Create your models here.

Factory = (
    ('factory1', 'factory1'),
    ('factory2', 'factory2'),
    ('factory3', 'factory3'),
    ('factory4', 'factory4'),
    ('factory5', 'factory5'),
)

Fabric_choices = (
    ('woven', 'Woven'),
    ('knit', 'Knit'),
    ('others', 'Others')
)

Wash = (
    ('non-wash', 'Non-Wash'),
    ('wash', 'Wash'),
)

Style = (
    ('formal', 'Formal'),
    ('casual', 'Casual'),
)


class GeneratePFM(models.Model):
    pfmno = models.CharField(max_length=50, primary_key=True)
    fabric = models.CharField(max_length=100, null=True)
    wash = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    sub_category = models.CharField(max_length=100, null=True)
    super_category = models.CharField(max_length=100, null=True)
    style_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.pfmno


class AddOperations(models.Model):
    pfmno = models.CharField(max_length=50, default="null")
    component = models.CharField(max_length=200, default="null")
    component_type = models.CharField(max_length=200, default="null")
    department = models.CharField(max_length=200, default="null")
    section = models.CharField(max_length=200, default="null")
    sub_section = models.CharField(max_length=200, default="null")
    operations = models.CharField(max_length=200, default="null")
    # complexity = models.CharField(max_length=100)
    spi = models.CharField(max_length=100, default="null")
    stitch_length = models.CharField(max_length=100, default="null")
    thread_consumption = models.CharField(max_length=100, default="null")
    machine_auto = models.CharField(max_length=100, default="null")
    work_aid = models.CharField(max_length=100, default="null")
    psmv = models.CharField(max_length=100, default="null")
    asmv = models.CharField(max_length=100, default="null")
    spi_factor = models.CharField(max_length=100, default="null")
    shade = models.CharField(max_length=100, default="null")
    thread_spec = models.CharField(max_length=100, default="null")
    pick_time = models.CharField(max_length=100, default="null")
    main_time = models.CharField(max_length=100, default="null")
    turn_time = models.CharField(max_length=100, default="null")
    dispose_time = models.CharField(max_length=100, default="null")
    operation_complexity = models.CharField(max_length=100, default="null")
    spi_complexity = models.CharField(max_length=100, default="null")
    stitch_complexity = models.CharField(max_length=100, default="null")
    personal = models.CharField(max_length=100, default="null")
    fatique = models.CharField(max_length=100, default="null")
    delay = models.CharField(max_length=100, default="null")
    psam = models.CharField(max_length=100, default="null")
    typee = models.CharField(max_length=100, default="null")
    pct = models.CharField(max_length=100, default="null")
    mpall = models.CharField(max_length=100, default="null")
    name = models.CharField(max_length=100, default="null")
    oph = models.CharField(max_length=100, default="null")
    act = models.CharField(max_length=100, default="null")
    grade = models.CharField(max_length=100, default="null")

    # sam = models.CharField(max_length=100)
    # allowance = models.CharField(max_length=100)

    def __str__(self):
        return self.pfmno


def __str__(self):
        return self.pfmno


class GenerateOB(models.Model):
    pfmno = models.CharField(max_length=50)
    orderno = models.CharField(max_length=50)
    styleno = models.CharField(max_length=50)
    lineno = models.CharField(max_length=50)
    shift = models.CharField(max_length=50)
    order_quantity = models.CharField(max_length=50)
    capacity = models.CharField(max_length=50)
    target = models.CharField(max_length=50)
    skill_level = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    subSection = models.CharField(max_length=50)
    collar = models.CharField(max_length=50, null=True)
    pocket = models.CharField(max_length=50, null=True)
    vent = models.CharField(max_length=50, null=True)
    lapel = models.CharField(max_length=50, null=True)
    cuff = models.CharField(max_length=50, null=True)
    sleeve = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.pfmno


class GOperationBul(models.Model):
    pfmno = models.CharField(max_length=50)
    mpnos = models.DecimalField(max_digits=8, default="0.00", decimal_places=5)
    mpallocation = models.IntegerField(default="1")
    oph = models.DecimalField(max_digits=8, default="0.00", decimal_places=5)
    Type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    cost = models.IntegerField(default="1")
    operation_id = models.CharField(max_length=50)
    orderno = models.CharField(max_length=50, default=" ")

    def __str__(self):
        return self.name
