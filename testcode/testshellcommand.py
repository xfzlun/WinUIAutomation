import os
#time_start = time.time()
cmd = "pdf2htmlEX --no-drm 1 --embed-css 0 --embed-image 0 --embed-font 0 --split-pages 1 --fit-width 748 --css-filename html.css --dest-dir %s --embed-external-font 0 --auto-hint 1 %s" % ('html_output_folder', 'src_file')
cmd_list = cmd.split(" ")
print(cmd_list)
print(type(cmd_list))
'''
    sub2 = subprocess.Popen(cmd_list)
    i = 0
    while 1:
        ret1 = subprocess.Popen.poll(sub2)
        if ret1 == 0:
            time_end = time.time()
            time_take = int(time_end - time_start + 0.5)
            with global_value_lock:
                success_ids[param[2]] = time_take
            print sub2.pid,'end'
            break
        elif ret1 is None:
            print  sub2.pid, 'running'
            if i >= max_check_time:
                time_end = time.time()
                time_take = int(time_end - time_start + 0.5)
                with global_value_lock:
                    timeout_ids[param[2]] = time_take
                sub2.kill()
                log_insert("%s%s%s" % (log_dir(output_folder), os.sep, "convert_log.txt"), src_file, "Timeout_Error", 'None')
                print "*****************Timeout_Error*****************"
                break
            time.sleep(check_time)
        else:
            time_end = time.time()
            time_take = int(time_end - time_start + 0.5)
            with global_value_lock:
                converterror_ids[param[2]] = time_take
            log_insert("%s%s%s" % (log_dir(output_folder), os.sep, "convert_log.txt"), src_file, "Process_Term_Error", str(ret1))
            print sub2.pid,'term', ret1, ret1
            break
        i += 1
'''