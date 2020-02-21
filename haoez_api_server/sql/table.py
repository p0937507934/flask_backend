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
    return Table(
        "nir_keylist",
        metadata,
        Column("NIR_data_id", Integer, primary_key=True, nullable=False),
        Column("NIR_datetime", DateTime),
        Column("NIR_Wave_type", VARCHAR(20)),
        Column("NIR_LAMP", Integer),
        Column("NIR_Wave_Range_start", Integer),
        Column("NIR_Wave_Range_end", Integer),
        Column("NIR_Wavelength_Width", Float),
        Column("NIR_Gain", Integer),
        Column("NIR_average", Integer),
        Column("NIR_Wavelength_Points", Integer),
        Column("Group_id", Integer, ForeignKey("group.Group_id")),
        Column("Camera_id", Integer, ForeignKey("camera_type.Camera_id")),
        Column("File_id", Integer, ForeignKey("filename.File_id")),
        extend_existing=True,
    )


def hp280_keylist(metadata):
    return Table(
        "hp280_keylist",
        metadata,
        Column("Hp280_data_id", Integer, primary_key=True, nullable=False),
        Column("Hp280_description", VARCHAR(100)),
        Column("Hp280_file_type", VARCHAR(10)),
        Column("Hp280_sensor_type", VARCHAR(10)),
        Column("Hp280_ihspt_version", VARCHAR(10)),
        Column("Hp280_interleave", VARCHAR(10)),
        Column("Hp280_samples", Integer),
        Column("Hp280_lines", Integer),
        Column("Hp280_bands", Integer),
        Column("Hp280_default_bands_1", Integer),
        Column("Hp280_default_bands_2", Integer),
        Column("Hp280_default_bands_3", Integer),
        Column("Hp280_header_offset", Integer),
        Column("Hp280_data_type", Integer),
        Column("Hp280_byte_order", Integer),
        Column("Hp280_x_start", Integer),
        Column("Hp280_y_start", Integer),
        Column("Hp280_max_value", Integer),
        Column("Hp280_fps", Float),
        Column("Hp280_tint", Float),
        Column("Hp280_acquisition_time", VARCHAR(30)),
        Column("Hp280_index", Integer),
        Column("Hp280_nr_frames", Integer),
        Column("Hp280_frames_lost", Integer),
        Column("Hp280_frames_lost_sw", Integer),
        Column("Hp280_exposure", Float),
        Column("Group_id", Integer, ForeignKey("group.Group_id")),
        Column("Camera_id", Integer, ForeignKey("camera_type.Camera_id")),
        Column("File_id", Integer, ForeignKey("filename.File_id")),
        extend_existing=True,
    )

def fx_keylist(metadata):
    return Table(
        "fx_keylist",
        metadata,
        Column("Fx_data_id", Integer, primary_key=True, nullable=False),
        Column("Fx_filetype", VARCHAR(20)),
        Column("FX_sensortype", VARCHAR(50)),
        Column("FX_acquisition_date", DateTime),
        Column("FX_qpfTiming_x", Float),
        Column("FX_qpfTiming_y", Float),
        Column("FX_interleave", VARCHAR(10)),
        Column("FX_samples", Integer),
        Column("FX_lines", Integer),
        Column("FX_bands", Integer),
        Column("FX_default_bands_R", Integer),
        Column("FX_default_bands_G", Integer),
        Column("FX_default_bands_B", Integer),
        Column("FX_header_offset", Integer),
        Column("FX_data_type", Integer),
        Column("FX_byte_order", Integer),
        Column("FX_x_start", Integer),
        Column("FX_y_start", Integer),
        Column("FX_fps", Float),
        Column("FX_binning_0", Integer),
        Column("FX_binning_1", Integer),
        Column("FX_vroi_0", Integer),
        Column("FX_vroi_1", Integer),
        Column("FX_hroi_0", Integer),
        Column("FX_hroi_1", Integer),
        Column("FX_vimg_0", Integer),
        Column("FX_vimg_1", Integer),
        Column("FX_sensorid", VARCHAR(20)),
        Column("FX_tint", Float),
        Column("FX_himg_0", Integer),
        Column("FX_himg_1", Integer),
        Column("FX_fodis_0", Integer),
        Column("FX_fodis_1", Integer),
        Column("FX_exposure", Integer),
        Column("FX_AD_type", Integer),
        Column("FX_Size_Factor", Float),
        Column("FX_errors", VARCHAR(20)),
        Column("Group_id", Integer, ForeignKey("group.Group_id")),
        Column("Camera_id", Integer, ForeignKey("camera_type.Camera_id")),
        Column("File_id", Integer, ForeignKey("filename.File_id")),
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
