# Meal menu recommendation website, EatMate
![group5-11](https://user-images.githubusercontent.com/66261167/148727861-b9df2066-32fa-41a4-ace9-63455727375a.png)
![group5-12](https://user-images.githubusercontent.com/66261167/148727869-50dab58f-ff7f-4e2f-97a6-396fa4c3f24c.png)
![group5-15](https://user-images.githubusercontent.com/66261167/148727884-22088139-57e3-443a-b7da-4558e0e6fa26.png)
![group5-13](https://user-images.githubusercontent.com/66261167/148727893-afc2913a-2494-4669-b1f0-612d47891a55.png)
![group5-14](https://user-images.githubusercontent.com/66261167/148727895-ca04216c-c749-46df-a0f7-2c916aa268f3.png)



> **Abstract:**  

> 점메추(점심메뉴추천)이라는 줄임말이 있을 정도로 식사 메뉴는 하루의 중요한 고민거리이다.  
> 따라서 사용자의 기호(단체 식사, 매운 음식, 다이어트 음식 등등)를 반영하여 식사 메뉴를 추천해주는 웹사이트를 구축하였다.  
> 코드는 `mysql`과 `python tkinter library`를 중점적으로 사용하였다.  
> 
> Meal menus are an important concern of the day to the extent that there is an abbreviation of "LMR(lunch menu recommendation)."
> Therefore, I established a website that recommends a meal menu by reflecting the user's preferences (group meal, spicy food, diet food, etc.).
> In code, `mysql` and `python tkinter library` were mainly used.
   
<Br>  

## How to Install
1. `conda`를 이용하여 가상환경 설치  
  Install virtual environment Using `conda`
  ```
  conda env create -n mysql -f environment.yaml
  conda activate mysql
  ```  
  <Br>  
  
2. mysql이 저장된 경로에 있거나  
  mysql이 저장된 경로가 환경변수로 설정된 경우, 다음 커맨드를 통해 mysql 로그인  
  If current directory is the path where mysql is stored or  
  the path where mysql is stored is set as an environmental variable, Log in mysql through the next command.
  ```
  mysql -u root -p
  ```    
  
  <Br>  
  
3. 다음 커맨드를 통해 mysql에 DB 생성  
  Create DB in mysql through the next command  
  ```
  source [eatmate-db-dumo.sql path]
  ```  
  <Br>  
  
4. mysql 종료  
  End mysql
  ```
  EXIT
  ```  
  <Br>  
  
5. `eatmate.py` 내에 전역변수 PW에 mysql root계정 비밀번호 할당  
   Assign mysql root account password in global variable PW in `eatmate.py`
   
## Usage

  ```
  python eatmate.py
  ```
    
## Citaion
If you refer to the code, please attach to the following phrase.
  ```
  Choi, S. M. (2021a). GitHub - saemee007/DBMS_menuReco: Mysql and python-based websites that recommend meal menus based on users’ preferences. GitHub. https://github.com/saemee007/DBMS_menuReco
  ```  
