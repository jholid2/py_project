import os, time
import re

class file_monitoring:
    def __init__(self, directory='./monitor_directory'):
        self.directory = directory
        self.file_t_f = False
        self.file_list = []
        self.target_extensions = ['.py', '.js', '.class']
        self.dangerous_files_content = []
        
        try:
            self.file_list = os.listdir(self.directory)
            print(f'해당 디렉터리에 존재하는 파일은 {self.file_list} 입니다.')
            self.file_t_f = True
        except FileNotFoundError:
            print('해당 디렉터리는 존재하지 않거나 경로가 잘못되었습니다.')
        except:
            print('에러가 발생했습니다.')

    def check_file(self):
        if not self.file_t_f:
            return 0
        
        new_files = []
        for file in os.listdir(self.directory):
            if file not in self.file_list:
                new_files.append(file)

        if new_files:
            print(f'새로운 파일이 감지되었습니다.\n 파일명: {new_files}')
            self.file_extension(new_files)
            self.file_list = os.listdir(self.directory)
            return new_files

    def file_extension(self, files):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in self.target_extensions:
                print(f"위험한 파일일 수 있습니다.")
                self.read_file_content(file)

    def read_file_content(self, filename):
        file_path = os.path.join(self.directory, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.dangerous_files_content.append(content)
                
                # 정규식 탐지 실행
                self.detect_patterns(filename, content)
        except:
            print('에러가 발생했습니다.')

    def detect_patterns(self, filename, content):
        print(f" {filename} 파일 탐지 결과 ")
        
        #주석 탐지
        comments = []
        # Python 주석
        python_comments = re.findall(r'#.*', content)
        comments.extend(python_comments)
        # JavaScript 한줄 주석
        js_comments = re.findall(r'//.*', content)
        comments.extend(js_comments)
        
        # 블록 주석
        block_comments = re.findall(r'/\*.*?\*/', content, re.DOTALL)
        comments.extend(block_comments)
        
        if comments:
            print(f"주석 발견: {len(comments)}개")
            for comment in comments:  # 전체 출력
                print(f"- {comment.strip()}")
        else:
            print("주석 없음")

        # 2. 이메일 탐지
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        
        if emails:
            print(f"이메일 발견: {len(emails)}개")
            for email in emails:
                print(f"- {email}")
        else:
            print("이메일 없음")

        # 3. SQL문 탐지
        sql_patterns = [
            r'\bSELECT\b.*?\bFROM\b.*?(?=;|\n|$)',
            r'\bINSERT\s+INTO\b.*?(?=;|\n|$)',
            r'\bUPDATE\b.*?\bSET\b.*?(?=;|\n|$)',
            r'\bDELETE\s+FROM\b.*?(?=;|\n|$)',
            r'\bCREATE\s+TABLE\b.*?(?=;|\n|$)',
            r'\bDROP\s+TABLE\b.*?(?=;|\n|$)'
        ]
        
        sql_queries = []
        for pattern in sql_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            sql_queries.extend(matches)
        
        if sql_queries:
            print(f"SQL문 발견: {len(sql_queries)}개")
            for sql in sql_queries:  # 전체 출력
                print(f"- {sql.strip()}")
        else:
            print("SQL문 없음")

    def auto_monitoring(self, sleep_sec=2):
        self.sleep_sec = sleep_sec
        print(f'모니터링을 시작합니다.{sleep_sec}초마다 진행됩니다.')
        try:
            while True:
                self.check_file()
                time.sleep(sleep_sec)
        except KeyboardInterrupt:
            print("\n***모니터링 프로그램 종료***")

a = file_monitoring()
a.auto_monitoring()