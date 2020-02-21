from sqlalchemy import Column, Table, Integer, Float, VARCHAR, DateTime, ForeignKey


def group(metadata):
    return Table(
        "group",
        metadata,
        Column("Group_id", Integer, primary_key=True, nullable=False),
        Column("Group_name", VARCHAR(20), nullable=False),
        Column("Group_password", VARCHAR(20), nullable=False),
        extend_existing=True,
    )


def nir_keylist(metadata):
    '''
    Todo: 確認vis-nir是否要建在此表或新建,還有SWNIR
    '''
    return Table(
        "nir_keylist",
        metadata,
        Column("NIR_data_id", Integer, primary_key=True, nullable=False),
        Column("Group_id", Integer, ForeignKey("group.Group_id")),
        Column("Camera_id", Integer, ForeignKey("camera_type.Camera_id")),
        Column("File_id", Integer, ForeignKey("filename.File_id")),
        Column("Sample_id", Integer, ForeignKey("sample_type.Sample_id")),
        extend_existing=True,
    )


def hp280_keylist(metadata):
    return Table(
        "hp280_keylist",
        metadata,
        Column("Hp280_data_id", Integer, primary_key=True, nullable=False),
        Column("Group_id", Integer, ForeignKey("group.Group_id")),
        Column("Camera_id", Integer, ForeignKey("camera_type.Camera_id")),
        Column("File_id", Integer, ForeignKey("filename.File_id")),
        Column("Sample_id", Integer, ForeignKey("sample_type.Sample_id")),
        extend_existing=True,
    )

def fx_keylist(metadata):
    return Table(
        "fx_keylist",
        metadata,
        Column("Fx_data_id", Integer, primary_key=True, nullable=False),
        Column("Group_id", Integer, ForeignKey("group.Group_id")),
        Column("Camera_id", Integer, ForeignKey("camera_type.Camera_id")),
        Column("File_id", Integer, ForeignKey("filename.File_id")),
        Column("Sample_id", Integer, ForeignKey("sample_type.Sample_id")),
        extend_existing=True,
    )


def algorithm_permission(metadata):
    return Table(
        "algorithm_permission",
        metadata,
        Column("Group_id", Integer, ForeignKey("group.Group_id")),
        Column("Algorithm_id", Integer, ForeignKey("algorithm.Algorithm_id")),
        extend_existing=True,
    )


def algorithm(metadata):
    return Table(
        "algorithm",
        metadata,
        Column("Algorithm_id", Integer, primary_key=True, nullable=False),
        Column("Algorithm_name", VARCHAR(20), nullable=False),
        extend_existing=True,
    )


def camera_type(metadata):
    return Table(
        "camera_type",
        metadata,
        Column("Camera_id", Integer, primary_key=True, nullable=False),
        Column("Camera_name", VARCHAR(20), nullable=False),
        extend_existing=True,
    )


def filename(metadata):
    return Table(
        "filename",
        metadata,
        Column("File_id", Integer, primary_key=True, nullable=False),
        Column("File_name", VARCHAR(50), nullable=False),
        Column("File_path", VARCHAR(50), nullable=False),
        Column("File_time", DateTime, nullable=False),
        extend_existing=True,
    )


def sample_type(metadata):
    return Table(
        "sample_type",
        metadata,
        Column("Sample_id", Integer, primary_key=True, nullable=False),
        Column("Sample_name", VARCHAR(50), nullable=False),
        extend_existing=True,
    )
