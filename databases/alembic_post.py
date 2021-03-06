# -*- coding: utf-8 -*-
#
# Script to be executed following an alembic update of the SQLite database
#
# Alembic is used to update the database schema. This script is used to
# execute code after all database schema updates have been performed, and
# typically involves database entry modifications.
#
# Note: Newest revision at the top
#
# The following code is also needed in the upgrade() function of the alembic
# upgrade script to indicate which section of this script to run. This should
# already be included in the alembic script template.
#
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(__file__, "../../../..")))
# from databases.alembic_post_utils import write_revision_post_alembic
# def upgrade():
#     write_revision_post_alembic(revision)
#
import sys
import traceback

import os

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))

from databases.alembic_post_utils import read_revision_file
from mycodo.config import ALEMBIC_UPGRADE_POST
from mycodo.config import SQL_DATABASE_MYCODO
from mycodo.databases.utils import session_scope


MYCODO_DB_PATH = 'sqlite:///' + SQL_DATABASE_MYCODO


if __name__ == "__main__":
    error = []
    print("Found revision IDs to execute code: {con}".format(
        con=read_revision_file()))

    for each_revision in read_revision_file():
        print("Revision ID {rev}".format(
            file=ALEMBIC_UPGRADE_POST, rev=each_revision))

        if not each_revision:
            print("Error: Revision ID empty")

        # elif each_revision == 'REPLACE_WITH_ALEMBIC_REVISION_ID':
        #     print("Executing post-alembic code for revision {}".format(
        #         each_revision))
        #     try:
        #         pass  # Code goes here
        #     except Exception:
        #         msg = "ERROR: post-alembic revision {}: {}".format(
        #             each_revision, traceback.format_exc())
        #         error.append(msg)
        #         print(msg)

        elif each_revision == 'd66e33093e8e':
            # convert database entries to JSON string for custom_options entry
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            import json
            from mycodo.databases.models import Widget
            try:
                with session_scope(MYCODO_DB_PATH) as session:
                    for each_widget in session.query(Widget).all():
                        custom_options = {}
                        if each_widget.graph_type == 'graph':
                            each_widget.graph_type = 'widget_graph_synchronous'
                            custom_options['measurements_math'] = each_widget.math_ids.split(";")
                            custom_options['measurements_note_tag'] = each_widget.note_tag_ids.split(";")
                            custom_options['measurements_input'] = each_widget.input_ids_measurements.split(";")
                            custom_options['measurements_output'] = each_widget.output_ids.split(";")
                            custom_options['measurements_pid'] = each_widget.pid_ids.split(";")
                        elif each_widget.graph_type == 'spacer':
                            each_widget.graph_type = 'widget_spacer'
                        elif each_widget.graph_type == 'gauge_angular':
                            each_widget.graph_type = 'widget_gauge_angular'
                            custom_options['measurement'] = each_widget.input_ids_measurements
                        elif each_widget.graph_type == 'gauge_solid':
                            each_widget.graph_type = 'widget_gauge_solid'
                            custom_options['measurement'] = each_widget.input_ids_measurements
                        elif each_widget.graph_type == 'indicator':
                            each_widget.graph_type = 'widget_indicator'
                            custom_options['measurement'] = each_widget.input_ids_measurements
                        elif each_widget.graph_type == 'measurement':
                            each_widget.graph_type = 'widget_measurement'
                            custom_options['measurement'] = each_widget.input_ids_measurements
                        elif each_widget.graph_type == 'output':
                            each_widget.graph_type = 'widget_output'
                            custom_options['output'] = each_widget.output_ids
                        elif each_widget.graph_type == 'output_pwm_slider':
                            each_widget.graph_type = 'widget_output_pwm_slider'
                            custom_options['output'] = each_widget.output_ids
                        elif each_widget.graph_type == 'pid_control':
                            each_widget.graph_type = 'widget_pid'
                            custom_options['pid'] = each_widget.pid_ids
                        elif each_widget.graph_type == 'camera':
                            each_widget.graph_type = 'widget_camera'

                        custom_options['refresh_seconds'] = each_widget.refresh_duration
                        custom_options['x_axis_minutes'] = each_widget.x_axis_duration
                        custom_options['custom_yaxes'] = each_widget.custom_yaxes.split(";")
                        custom_options['decimal_places'] = each_widget.decimal_places
                        custom_options['enable_status'] = each_widget.enable_status
                        custom_options['enable_value'] = each_widget.enable_value
                        custom_options['enable_name'] = each_widget.enable_name
                        custom_options['enable_unit'] = each_widget.enable_unit
                        custom_options['enable_measurement'] = each_widget.enable_measurement
                        custom_options['enable_channel'] = each_widget.enable_channel
                        custom_options['enable_timestamp'] = each_widget.enable_timestamp
                        custom_options['enable_navbar'] = each_widget.enable_navbar
                        custom_options['enable_rangeselect'] = each_widget.enable_rangeselect
                        custom_options['enable_export'] = each_widget.enable_export
                        custom_options['enable_title'] = each_widget.enable_title
                        custom_options['enable_auto_refresh'] = each_widget.enable_auto_refresh
                        custom_options['enable_xaxis_reset'] = each_widget.enable_xaxis_reset
                        custom_options['enable_manual_y_axis'] = each_widget.enable_manual_y_axis
                        custom_options['enable_start_on_tick'] = each_widget.enable_start_on_tick
                        custom_options['enable_end_on_tick'] = each_widget.enable_end_on_tick
                        custom_options['enable_align_ticks'] = each_widget.enable_align_ticks
                        custom_options['use_custom_colors'] = each_widget.use_custom_colors
                        custom_options['custom_colors'] = each_widget.custom_colors.split(",")
                        custom_options['range_colors'] = each_widget.range_colors.split(";")
                        custom_options['disable_data_grouping'] = each_widget.disable_data_grouping.split(",")
                        custom_options['max_measure_age'] = each_widget.max_measure_age
                        custom_options['stops'] = each_widget.stops
                        custom_options['min'] = each_widget.y_axis_min
                        custom_options['max'] = each_widget.y_axis_max
                        custom_options['option_invert'] = each_widget.option_invert
                        custom_options['font_em_name'] = each_widget.font_em_name
                        custom_options['font_em_value'] = each_widget.font_em_value
                        custom_options['font_em_timestamp'] = each_widget.font_em_timestamp
                        custom_options['enable_output_controls'] = each_widget.enable_output_controls
                        custom_options['show_pid_info'] = each_widget.show_pid_info
                        custom_options['show_set_setpoint'] = each_widget.show_set_setpoint
                        custom_options['camera_id'] = each_widget.camera_id
                        custom_options['camera_image_type'] = each_widget.camera_image_type
                        custom_options['max_age'] = each_widget.camera_max_age
                        each_widget.custom_options = json.dumps(custom_options)
                        session.commit()
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '4d3258ef5864':
            # The post-script for 4ea0a59dee2b didn't work to change minute to s
            # This one works
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import DeviceMeasurements
                from mycodo.databases.models import Output

                with session_scope(MYCODO_DB_PATH) as session:
                    for each_output in session.query(Output).all():
                        if each_output.output_type == 'atlas_ezo_pmp':
                            measurements = session.query(DeviceMeasurements).filter(
                                DeviceMeasurements.device_id == each_output.unique_id).all()
                            for meas in measurements:
                                if meas.unit == 'minute':
                                    meas.unit = 's'
                                    session.commit()
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '4ea0a59dee2b':
            # Only LCDs with I2C interface were supported until this revision.
            # "interface" column added in this revision.
            # Sets all current interfaces to I2C.
            # Atlas Scientific pump output duration measurements are set to minute.
            # Change unit minute to the SI unit second, like other outputs.
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import DeviceMeasurements
                from mycodo.databases.models import LCD
                from mycodo.databases.models import Output

                with session_scope(MYCODO_DB_PATH) as session:
                    for meas in session.query(DeviceMeasurements).all():
                        if meas.measurement == 'acceleration_g_force':
                            meas.measurement = 'acceleration'
                        elif meas.measurement == 'acceleration_x_g_force':
                            meas.measurement = 'acceleration_x'
                        elif meas.measurement == 'acceleration_y_g_force':
                            meas.measurement = 'acceleration_y'
                        elif meas.measurement == 'acceleration_z_g_force':
                            meas.measurement = 'acceleration_z'
                        session.commit()

                    outputs = session.query(Output).filter(
                        Output.output_type == 'atlas_ezo_pmp').all()
                    for each_output in outputs:
                        measurements = session.query(DeviceMeasurements).filter(
                            DeviceMeasurements.device_id == each_output.unique_id).all()
                        for meas in measurements:
                            if meas.unit == 'minute':
                                meas.unit = 's'
                                session.commit()

                    for lcd in session.query(LCD).all():
                        lcd.interface = 'I2C'
                        session.commit()

            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == 'af5891792291':
            # Set the output_type for PID controller outputs
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.utils.outputs import parse_output_information
                from mycodo.databases.models import DeviceMeasurements
                from mycodo.databases.models import Output
                from mycodo.databases.models import PID

                dict_outputs = parse_output_information()

                with session_scope(MYCODO_DB_PATH) as session:
                    for each_pid in session.query(PID).all():
                        try:
                            new_measurement = DeviceMeasurements()
                            new_measurement.name = "Output (Volume)"
                            new_measurement.device_id = each_pid.unique_id
                            new_measurement.measurement = 'volume'
                            new_measurement.unit = 'ml'
                            new_measurement.channel = 8
                            session.add(new_measurement)

                            if each_pid.raise_output_id:
                                output_raise = session.query(Output).filter(
                                    Output.unique_id == each_pid.raise_output_id).first()
                                if output_raise:  # Use first output type listed (default)
                                    each_pid.raise_output_type = dict_outputs[output_raise.output_type]['output_types'][0]
                            if each_pid.lower_output_id:
                                output_lower = session.query(Output).filter(
                                    Output.unique_id == each_pid.lower_output_id).first()
                                if output_lower:  # Use first output type listed (default)
                                    each_pid.lower_output_type = dict_outputs[output_lower.output_type]['output_types'][0]
                            session.commit()
                        except:
                            msg = "ERROR-1: post-alembic revision {}: {}".format(
                                each_revision, traceback.format_exc())
                            error.append(msg)
                            print(msg)

            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '561621f634cb':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import DeviceMeasurements
                from mycodo.databases.models import Output
                from mycodo.utils.outputs import parse_output_information

                dict_outputs = parse_output_information()

                with session_scope(MYCODO_DB_PATH) as session:
                    for each_output in session.query(Output).all():

                        if not session.query(DeviceMeasurements).filter(
                                DeviceMeasurements.device_id == each_output.unique_id).first():
                            # No output device measurements exist. Need to create them.
                            if ('measurements_dict' in dict_outputs[each_output.output_type] and
                                    dict_outputs[each_output.output_type]['measurements_dict'] != []):
                                for each_channel in dict_outputs[each_output.output_type]['measurements_dict']:
                                    measure_info = dict_outputs[each_output.output_type]['measurements_dict'][each_channel]
                                    new_measurement = DeviceMeasurements()
                                    if 'name' in measure_info:
                                        new_measurement.name = measure_info['name']
                                    new_measurement.device_id = each_output.unique_id
                                    new_measurement.measurement = measure_info['measurement']
                                    new_measurement.unit = measure_info['unit']
                                    new_measurement.channel = each_channel
                                    session.add(new_measurement)

                        session.commit()
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '61a0d0568d24':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import Role

                with session_scope(MYCODO_DB_PATH) as session:
                    for role in session.query(Role).all():
                        if role.name in ['Kiosk', 'Guest']:
                            role.reset_password = False
                        else:
                            role.reset_password = True
                        session.commit()
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == 'f5b77ef5f17c':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import SMTP

                with session_scope(MYCODO_DB_PATH) as session:
                    for smtp in session.query(SMTP).all():
                        error = []
                        if smtp.ssl:
                            smtp.protocol = 'ssl'
                            if smtp.port == 465:
                                smtp.port = None
                        elif not smtp.ssl:
                            smtp.protocol = 'tls'
                            if smtp.port == 587:
                                smtp.port = None
                        else:
                            smtp.protocol = 'unencrypted'
                        if not error:
                            session.commit()
                        else:
                            for each_error in error:
                                print("Error: {}".format(each_error))
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '0a8a5eb1be4b':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import Input

                with session_scope(MYCODO_DB_PATH) as session:
                    for each_input in session.query(Input).all():
                        error = []
                        if each_input.device == 'DS18B20' and 'library,ow_shell' in each_input.custom_options:
                            each_input.device = 'DS18B20_OWS'
                        each_input.custom_options = ''
                        if not error:
                            session.commit()
                        else:
                            for each_error in error:
                                print("Error: {}".format(each_error))
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '55aca47c2362':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import Widget
                from mycodo.databases.models import Dashboard

                with session_scope(MYCODO_DB_PATH) as session:
                    new_dash = Dashboard()
                    new_dash.name = 'Default Dashboard'
                    session.add(new_dash)

                    for each_widget in session.query(Widget).all():
                        each_widget.dashboard_id = new_dash.unique_id
                        session.commit()

                    if not error:
                        session.commit()
                    else:
                        for each_error in error:
                            print("Error: {}".format(each_error))
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '895ddcdef4ce':
            # Add PID setpoint_tracking_type and setpoint_tracking_id
            # If method_id set, set setpoint_tracking_type to 'method;
            # and copy method_id to new setpoint_tracking_id.
            # PID.method_id deleted after executing this code.
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import PID

                with session_scope(MYCODO_DB_PATH) as session:
                    for each_pid in session.query(PID).all():
                        error = []
                        if each_pid.setpoint_tracking_id:
                            each_pid.setpoint_tracking_type = 'method'
                        if not error:
                            session.commit()
                        else:
                            for each_error in error:
                                print("Error: {}".format(each_error))
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '0ce53d526f13':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import Actions
                from mycodo.databases.models import Conditional
                from mycodo.utils.conditional import save_conditional_code

                conditions = conditional_sess.query(ConditionalConditions).all()
                actions = conditional_sess.query(Actions).all()

                with session_scope(MYCODO_DB_PATH) as cond_sess:
                    for each_cond in cond_sess.query(Conditional).all():
                        error = []
                        each_cond.conditional_statement = each_cond.conditional_statement.replace(
                            'self.measure(', 'self.condition(')
                        each_cond.conditional_statement = each_cond.conditional_statement.replace(
                            'self.measure_dict(', 'self.condition_dict(')
                        if not error:
                            cond_sess.commit()
                        else:
                            for each_error in error:
                                print("Error: {}".format(each_error))

                        save_conditional_code(
                            [],
                            each_cond.conditional_statement,
                            each_cond.unique_is,
                            conditions,
                            actions)
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '545744b31813':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import Output

                with session_scope(MYCODO_DB_PATH) as output_sess:
                    for each_output in output_sess.query(Output).all():
                        if each_output.measurement == 'time':
                            each_output.measurement = 'duration_time'
                            output_sess.commit()
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '802cc65f734e':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:  # Check if already installed
                import Pyro5.api
            except Exception:  # Not installed. Try to install
                try:
                    from mycodo.config import INSTALL_DIRECTORY
                    import subprocess
                    command = '{path}/env/bin/pip install -r {path}/install/requirements.txt'.format(
                        path=INSTALL_DIRECTORY)
                    cmd = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                    cmd_out, cmd_err = cmd.communicate()
                    cmd_status = cmd.wait()
                    import Pyro5.api
                except Exception:
                    msg = "ERROR: post-alembic revision {}: {}".format(
                        each_revision, traceback.format_exc())
                    error.append(msg)
                    print(msg)

        elif each_revision == '2e416233221b':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import Dashboard
                from mycodo.databases.models import DeviceMeasurements
                from mycodo.databases.models import Output
                from mycodo.config import OUTPUT_INFO

                output_unique_id = {}
                # Go through each output to get output unique_id
                with session_scope(MYCODO_DB_PATH) as output_sess:
                    for each_output in output_sess.query(Output).all():
                        output_unique_id[each_output.unique_id] = []

                        # Create measurements in device_measurements table
                        for measurement, measure_data in OUTPUT_INFO[each_output.output_type]['measure'].items():
                            for unit, unit_data in measure_data.items():
                                for channel, channel_data in unit_data.items():
                                    new_measurement = DeviceMeasurements()
                                    new_measurement.device_id = each_output.unique_id
                                    new_measurement.name = ''
                                    new_measurement.is_enabled = True
                                    new_measurement.measurement = measurement
                                    new_measurement.unit = unit
                                    new_measurement.channel = channel
                                    output_sess.add(new_measurement)
                                    output_sess.commit()

                                    output_unique_id[each_output.unique_id].append(
                                        new_measurement.unique_id)

                    # Update all outputs in Dashboard elements to new unique_ids
                    for each_dash in output_sess.query(Dashboard).all():
                        each_dash.output_ids = each_dash.output_ids.replace(',output', '')
                        output_sess.commit()

                        for each_output_id, list_device_ids in output_unique_id.items():
                            id_string = ''
                            for index, each_device_id in enumerate(list_device_ids):
                                id_string += '{},{}'.format(each_output_id, each_device_id)
                                if index + 1 < len(list_device_ids):
                                    id_string += ';'

                            if each_output_id in each_dash.output_ids:
                                each_dash.output_ids = each_dash.output_ids.replace(
                                    each_output_id, id_string)
                                output_sess.commit()
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == 'ef49f6644e0c':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import Actions
                from mycodo.databases.models import Conditional
                from mycodo.databases.models import Input
                from mycodo.inputs.python_code import execute_at_creation
                from mycodo.utils.conditional import save_conditional_code

                conditions = conditional_sess.query(ConditionalConditions).all()
                actions = conditional_sess.query(Actions).all()

                with session_scope(MYCODO_DB_PATH) as conditional_sess:
                    for each_conditional in conditional_sess.query(Conditional).all():
                        save_conditional_code(
                            [],
                            each_conditional.conditional_statement,
                            each_conditional.unique_is,
                            conditions,
                            actions)

                with session_scope(MYCODO_DB_PATH) as input_sess:
                    for each_input in input_sess.query(Input).all():
                        if each_input.device == 'PythonCode' and each_input.cmd_command:
                            try:
                                execute_at_creation(each_input.unique_id,
                                                    each_input.cmd_command,
                                                    None)
                            except Exception as msg:
                                print("Exception: {}".format(msg))
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '65271370a3a9':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import Actions
                from mycodo.databases.models import Conditional
                from mycodo.databases.models import Input
                from mycodo.inputs.python_code import execute_at_creation
                from mycodo.utils.conditional import save_conditional_code

                conditions = conditional_sess.query(ConditionalConditions).all()
                actions = conditional_sess.query(Actions).all()

                # Conditionals
                with session_scope(MYCODO_DB_PATH) as conditional_sess:
                    for each_conditional in conditional_sess.query(Conditional).all():
                        if each_conditional.conditional_statement:
                            # Replace strings
                            try:
                                strings_replace = [
                                    ('measure(', 'self.measure('),
                                    ('measure_dict(', 'self.measure_dict('),
                                    ('run_action(', 'self.run_action('),
                                    ('run_all_actions(', 'self.run_all_actions('),
                                    ('=message', '=self.message'),
                                    ('= message', '= self.message'),
                                    ('message +=', 'self.message +='),
                                    ('message+=', 'self.message+=')
                                ]
                                for each_set in strings_replace:
                                    if each_set[0] in each_conditional.conditional_statement:
                                        each_conditional.conditional_statement = each_conditional.conditional_statement.replace(
                                            each_set[0], each_set[1])
                            except Exception as msg:
                                print("Exception: {}".format(msg))

                        conditional_sess.commit()

                        save_conditional_code(
                            [],
                            each_conditional.conditional_statement,
                            each_conditional.unique_is,
                            conditions,
                            actions)

                # Inputs
                with session_scope(MYCODO_DB_PATH) as input_sess:
                    for each_input in input_sess.query(Input).all():
                        if each_input.device == 'PythonCode' and each_input.cmd_command:
                            # Replace strings
                            try:
                                strings_replace = [
                                    ('store_measurement(', 'self.store_measurement(')
                                ]
                                for each_set in strings_replace:
                                    if each_set[0] in each_input.cmd_command:
                                        each_input.cmd_command = each_input.cmd_command.replace(
                                            each_set[0], each_set[1])
                            except Exception as msg:
                                print("Exception: {}".format(msg))

                    input_sess.commit()

                    for each_input in input_sess.query(Input).all():
                        if each_input.device == 'PythonCode' and each_input.cmd_command:
                            try:
                                execute_at_creation(each_input.unique_id,
                                                    each_input.cmd_command,
                                                    None)
                            except Exception as msg:
                                print("Exception: {}".format(msg))
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == '70c828e05255':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import Conditional
                from mycodo.databases.models import ConditionalConditions

                with session_scope(MYCODO_DB_PATH) as conditional_sess:
                    for each_conditional in conditional_sess.query(Conditional).all():
                        if each_conditional.conditional_statement:

                            # Get conditions for this conditional
                            with session_scope(MYCODO_DB_PATH) as condition_sess:
                                for each_condition in condition_sess.query(ConditionalConditions).all():
                                    # Replace {ID} with measure("{ID}")
                                    id_str = '{{{id}}}'.format(id=each_condition.unique_id.split('-')[0])
                                    new_str = 'measure("{{{id}}}")'.format(id=each_condition.unique_id.split('-')[0])
                                    if id_str in each_conditional.conditional_statement:
                                        each_conditional.conditional_statement = each_conditional.conditional_statement.replace(
                                            id_str, new_str)

                                    # Replace print(1) with run_all_actions()
                                    new_str = 'run_all_actions()'
                                    if id_str in each_conditional.conditional_statement:
                                        each_conditional.conditional_statement = each_conditional.conditional_statement.replace(
                                            'print(1)', new_str)
                                        each_conditional.conditional_statement = each_conditional.conditional_statement.replace(
                                            'print("1")', new_str)
                                        each_conditional.conditional_statement = each_conditional.conditional_statement.replace(
                                            "print('1')", new_str)

                    conditional_sess.commit()
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        elif each_revision == 'b4d958997cf0':
            print("Executing post-alembic code for revision {}".format(
                each_revision))
            try:
                from mycodo.databases.models import Input

                with session_scope(MYCODO_DB_PATH) as new_session:
                    for each_input in new_session.query(Input).all():
                        if each_input.device in ['DS18B20', 'DS18S20']:
                            if 'library' not in each_input.custom_options:
                                if each_input.custom_options in [None, '']:
                                    each_input.custom_options = 'library,w1thermsensor'
                                else:
                                    each_input.custom_options += ';library,w1thermsensor'

                    new_session.commit()
            except Exception:
                msg = "ERROR: post-alembic revision {}: {}".format(
                    each_revision, traceback.format_exc())
                error.append(msg)
                print(msg)

        else:
            print("Code for revision {} not found".format(each_revision))

    if error:
        print("Completed with errors. Review the entire log for details.")
    else:
        try:
            print("Completed without errors. Deleting {}".format(
                ALEMBIC_UPGRADE_POST))
            os.remove(ALEMBIC_UPGRADE_POST)
        except Exception:
            msg = "ERROR: Could not delete {}: {}".format(
                ALEMBIC_UPGRADE_POST, traceback.format_exc())
