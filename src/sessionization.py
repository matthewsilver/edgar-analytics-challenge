import sys
import time


class Session():
    def __init__(self, *filepaths):
        try:
            inactivity_period_file = open(filepaths[0], "r")
            self.timeout = int(inactivity_period_file.read())
            self.input_log_path = filepaths[1]
            self.output_path = filepaths[2]
            self.all_sessions = None
        except:
            raise

    def compute_session(self):
        session_count = 0
        all_sessions = []
        sessions_current = {}
        current_timestamp = 0
        current_time_raw = 0
        with open(self.input_log_path) as f:
            header = f.readline().split(',')
            field_idx = dict([(value, key) for key, value in dict(enumerate(header)).items()])
            for row in f:
                try:
                    data = row.split(',')
                    ip, date, time_clock, cik, accession, extension = \
                    data[field_idx['ip']], data[field_idx['date']], data[field_idx['time']], data[field_idx['cik']], data[field_idx['accession']], data[field_idx['extention']]
                    time_raw = f"{date} {time_clock}"
                    timestamp = time.strptime(time_raw, "%Y-%m-%d %H:%M:%S")

                    # new timestamp found; end session of anyone inactive long enough
                    if timestamp != current_timestamp:
                        for session in list(sessions_current):
                            current_timestamp_secs = time.mktime(current_timestamp)
                            if current_timestamp_secs - time.mktime(sessions_current[session]['most_recent_access']) >= self.timeout:
                                sessions_current[session]['session_length'] = int(time.mktime(sessions_current[session]['most_recent_access']) - time.mktime(sessions_current[session]['first_access']))
                                output_line = [
                                    session,
                                    sessions_current[session]['first_access_raw'],
                                    sessions_current[session]['most_recent_access_raw'],
                                    sessions_current[session]['duration'],
                                    str(sessions_current[session]['document_count'])
                                ]
                                all_sessions.append(','.join([str(s) for s in output_line]))
                                sessions_current.pop(session)
                        current_timestamp = timestamp
                        current_time_raw = time_raw

                    # someone started a new session
                    if ip not in sessions_current:
                        sessions_current[ip] = {}
                        sessions_current[ip]['first_access_raw'] = time_raw
                        sessions_current[ip]['first_access'] = timestamp
                        sessions_current[ip]['most_recent_access'] = timestamp
                        sessions_current[ip]['most_recent_access_raw'] = time_raw
                        sessions_current[ip]['document_count'] = 1
                        sessions_current[ip]['duration'] = 1

                    # someone is continuing in a session; update their info
                    else:
                        sessions_current[ip]['document_count'] += 1
                        sessions_current[ip]['most_recent_access'] = timestamp
                        sessions_current[ip]['most_recent_access_raw'] = time_raw
                        sessions_current[ip]['duration'] = int(time.mktime(timestamp) - time.mktime(sessions_current[ip]['first_access']) + 1)
                except:
                    raise

        # if there are any active sessions at the end of file, write out in current state
        for session in sessions_current:
            output_line = [
                session,
                sessions_current[session]['first_access_raw'],
                sessions_current[session]['most_recent_access_raw'],
                sessions_current[session]['duration'],
                str(sessions_current[session]['document_count'])
            ]
            all_sessions.append(','.join([str(s) for s in output_line]))

        self.all_sessions = all_sessions

    def log_sessions(self):
        with open(self.output_path, 'w') as f:
            f.writelines(f"{session}\n" for session in self.all_sessions)


def main():
    filepaths = sys.argv[1:]
    session = Session(*filepaths)
    session.compute_session()
    session.log_sessions()


if __name__ == '__main__':
    main()