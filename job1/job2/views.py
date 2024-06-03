from django.shortcuts import render, redirect
from .models import TestBulk, TestBulk2
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


def table_test(request):

    return render(request, 'job2/table_test.html')


def test2(request):
    context = {
        'list' : TestBulk.objects.all(),
        'action_key' : '초기화면'
    }

    # df1이라는 dataframe을 만들기 위한 것임. 원래 DB와 같은 형태의 dataframe을 만들어서 사용함.
    original_rows=TestBulk.objects.all()

    # data_list라는 리스트는 딕셔너리로 구성되어 있으며, 각 column name에 맞게 값들이 list화 되어있음.
    data_list = [{'name' : rows.name, 'address' : rows.address, 'dept': rows.dept} for rows in original_rows]

    # datalist 리스트를 이용해 dataframe df1생성. df1는 초기 DB값을 복사한 것이다.
    df1 = pd.DataFrame(data_list)

    # df2는 사용자 UI에서 받아올 dataframe이다. 선언만 해준다.
    df2 = pd.DataFrame()

    if request.method == 'POST':

        action = request.POST['action']

        if action == 'action1': # 저장 버튼 누를 경우: 최종 결과값을 DB에 저장한다.
        #dataframe df2 초기 선언. df2는 UI의 최종 입력값이다.(추가 제외)

            # 각각 input을 list로 받는다. 곧 이것을 dataframe으로 만들 것이다.
            input_values_name = request.POST.getlist('name')
            input_values_address = request.POST.getlist('address')
            input_values_dept = request.POST.getlist('dept')
            
            result = zip(input_values_name, input_values_address, input_values_dept)

            for i, j, k in result:
                new_rows = [{'name':i, 'address':j, 'dept':k}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)

            # df_left는 df1에는 있는데 df2에는 없는 것이다.(수정했거나 삭제한 것), df_right은 df2에는 있는데 df1에는 없는 것이다.(수정했거나 추가한 것)
            df_left = pd.merge(df1, df2, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge']).reset_index(drop=True)
            df_right = pd.merge(df1, df2, how='outer', indicator=True).query('_merge == "right_only"').drop(columns=['_merge']).reset_index(drop=True)

            print(df_left)
            print(df_right)
            # 먼저 df_left를 다룬다.
            for i in range(0, len(df_left)):
                # df_right의 name column 내에 df_left의 1열 값이 들어가 있는가? 를 확인하는 logic
                is_same = df_right['name'] == df_left.iloc[i, 0]

                # 수정했으면 df_left에도 있을 것이고 df_right에도 있을 것이다.
                if is_same.sum() > 0:
                    
                    #df1을 다룬다(DB쪽)
                    for j in range (1, len(df1.columns)):
                        column_name = df1.columns[j]

                        # df2의 해당되는 행의 값과 Testbulk(DB)를 비교해서 바뀐 것이 있으면 바꾼다. 열은 바뀌지 않는다.
                        # row_to_update는 TestBulk 테이블에서 pk값이 df_left즉 바뀌어야 하는 것만 빼놓은 df에서 i행 0열값, 즉 name과 같은 row가 row_to_update
                        row_to_update = TestBulk.objects.get(pk=df_left.iloc[i,0])

                        #df2의 name값이 df_left.iloc[i,0](df_left는 수정해야되는 값만 있는 df지)인 행을 찾아서 그 행이 어딘지 알아냄.
                        n = int(df2[df2['name'] == df_left.iloc[i,0]].index[0])
                        
                        print(column_name)
                        print(n, j)
                        
                        #그래서 df2의 n행 j열 값을 알아내서 그걸 row_to_update에다가 넣을 것임
                        setattr(row_to_update, column_name, str(df2.iloc[n,j]))
                        row_to_update.save()

                # 삭제했으면 df_left에는 있고 df_right에는 없을 것이다.
                else:
                    row_to_delete = TestBulk.objects.get(pk=df_left.iloc[i, 0])
                    row_to_delete.delete()

            # df_right을 다룬다.
            for i in range(0, len(df_right)):
                # df_left의 name column 내에 df_right의 i열 값이 들어가 있는가?
                is_same = df_left['name'] == df_right.iloc[i, 0]

                # 수정했으면 df_left에도 있을 것이고 df_right에도 있을 것이다.
                if is_same.sum() == 0: # 추가라면, is_same값은 0일 것이다. df_right 에만 있고 df_left에는 없는 것이다.
                    # TeskBulk 모델 형태의 새로운 row인 row_to_plus를 생성해준다.
                    row_to_plus = TestBulk()
                    # TeskBulk의 새로운 행에 데이터를 넣어준다.
                    row_to_plus.name = df_right.iloc[i, 0]
                    row_to_plus.address = df_right.iloc[i, 1]
                    row_to_plus.dept = df_right.iloc[i, 2]
                    row_to_plus.save()
                else:
                    is_same = 1

        elif action == 'action2': #추가 버튼 누를 경우: 실제로는 추가하기 위한 key값만 넘겨준다. 그리고 html에서 추가를 위한 입력란을 형성한다. 
            
            # 추가 버튼을 누르면, UI에 있는 input들을 일단은 임시저장 상태로 만들고 그걸 이용해 df를 만들어서 다시 뿌려준다.
            input_values_name = request.POST.getlist('name')
            input_values_address = request.POST.getlist('address')
            input_values_dept = request.POST.getlist('dept')
            
            result = zip(input_values_name, input_values_address, input_values_dept)

            for i, j, k in result:
                new_rows = [{'name':i, 'address':j, 'dept':k}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)
            
            context = {
                'list2' : df2,
                'action_key' : '추가'
            }

        elif action == 'action3': #등록 버튼 누를 경우: 추가했던 추가 칸이 합쳐진다.

            # 등록 버튼을 누르면 지금까지 수정, 추가했던 내용을 df2로 만들어주고 UI에 보낸다. 그러면 추가된 값도 input_values가 된다!
            input_values_name = request.POST.getlist('name')
            input_values_address = request.POST.getlist('address')
            input_values_dept = request.POST.getlist('dept')

            result = zip(input_values_name, input_values_address, input_values_dept)

            for i, j, k in result:
                new_rows = [{'name':i, 'address':j, 'dept':k}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)

            name_new = request.POST['name_new']
            address_new = request.POST['address_new']
            dept_new = request.POST['dept_new']

            if name_new == "none" : # name_new라는 것이 없을수도 있는데 없는대로 그냥 두면 multivaluerror 발생함. 따라서 none일 상황을 html에서 만들어준다.
                context = {
                'list2' : df2,
                'action_key' : '등록'
            }
            else : # name_new는 새로운 줄이다. 새로운 줄을 df2에 추가해준다.
                new_rows_new = [{'name': name_new, 'address': address_new, 'dept': dept_new}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows_new)], ignore_index=True)
                context = {
                'list2' : df2,
                'action_key' : '등록'
            }

        elif action == 'action4': #삭제 버튼을 누를 경우: df2에서 해당 선택한 라인을 지워주고 다시 보내준다.
            #multivalueDictkeyerror 해결방법
            if 'radio_name' in request.POST:
                del_target_name = request.POST["radio_name"] #삭제 버튼 누르면, 라디오 버튼의 선택값(radio_name, 즉 이름)을 넘겨받는다.
                
                # 일단 df2는 만들어주고, 그 후에 삭제 해당하는 것을 df2에서 없애주자.
                input_values_name = request.POST.getlist('name')
                input_values_address = request.POST.getlist('address')
                input_values_dept = request.POST.getlist('dept')
                
                result = zip(input_values_name, input_values_address, input_values_dept)

                for i, j, k in result:
                    new_rows = [{'name':i, 'address':j, 'dept':k}]
                    df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)
                
                # 삭제를 df2에서만 해준다.
                name_idx = df2[df2['name']==del_target_name].index
                df2 = df2.drop(name_idx)

                context = {
                    'list2' : df2,
                    'action_key' : '삭제'
                }
            else:
                context = {

                }

    return render(request, 'job2/test2.html', context)


def test3(request):

    context = {
        'value' : '동작전'
    }

    if 'action1' in request.POST:
        
        selected = request.POST["select_options"]

        context = {
            'value' : selected, 
            'text' : '셀렉트'
        }

    if 'action2' in request.POST:
        
        selected = request.POST["select_options"]

        context = {
            'value' : selected,
            'text' : '버튼1'
        }

    if 'action3' in request.POST:
        
        selected = request.POST["select_options"]

        context = {
            'value' : selected,
            'text' : '버튼2'
        }


    return render(request, 'job2/test3.html', context)


def test4(request):

    context = {
        'list' : TestBulk.objects.all(),
        'action_key' : '초기화면'
    }

    # df1이라는 dataframe을 만들기 위한 것임. 원래 DB와 같은 형태의 dataframe을 만들어서 사용함.
    original_rows=TestBulk.objects.all()

    # data_list라는 리스트는 딕셔너리로 구성되어 있으며, 각 column name에 맞게 값들이 list화 되어있음.
    data_list = [{'name' : rows.name, 'address' : rows.address, 'dept': rows.dept} for rows in original_rows]

    # datalist 리스트를 이용해 dataframe df1생성. df1는 초기 DB값을 복사한 것이다.
    df1 = pd.DataFrame(data_list)

    # df2는 사용자 UI에서 받아올 dataframe이다. 선언만 해준다.
    df2 = pd.DataFrame()

    if request.method == 'POST':

        action = request.POST['action']

        if action == 'action1': # 저장 버튼 누를 경우: 최종 결과값을 DB에 저장한다.
        #dataframe df2 초기 선언. df2는 UI의 최종 입력값이다.(추가 제외)

            # 각각 input을 list로 받는다. 곧 이것을 dataframe으로 만들 것이다.
            input_values_name = request.POST.getlist('name')
            input_values_address = request.POST.getlist('address')
            input_values_dept = request.POST.getlist('dept')
            
            result = zip(input_values_name, input_values_address, input_values_dept)

            for i, j, k in result:
                new_rows = [{'name':i, 'address':j, 'dept':k}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)

            # df_left는 df1에는 있는데 df2에는 없는 것이다.(수정했거나 삭제한 것), df_right은 df2에는 있는데 df1에는 없는 것이다.(수정했거나 추가한 것)
            df_left = pd.merge(df1, df2, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge']).reset_index(drop=True)
            df_right = pd.merge(df1, df2, how='outer', indicator=True).query('_merge == "right_only"').drop(columns=['_merge']).reset_index(drop=True)

            # 먼저 df_left를 다룬다.
            for i in range(0, len(df_left)):
                # df_right의 name column 내에 df_left의 1열 값이 들어가 있는가?
                is_same = df_right['name'] == df_left.iloc[i, 0]

                # 수정했으면 df_left에도 있을 것이고 df_right에도 있을 것이다.
                if is_same.sum() > 0:

                    for j in range (0, len(df1.columns)):
                        column_name = df1.columns[j]

                        # df2의 해당되는 행의 값과 Testbulk를 비교해서 바뀐 것이 있으면 바꾼다. 열은 바뀌지 않는다.
                        row_to_update = TestBulk.objects.get(pk=df_left.iloc[i,0])

                        n = int(df2[df2['name'] == df_left.iloc[i,0]].index[0])
                        setattr(row_to_update, column_name, str(df2.iloc[n,j]))
                        row_to_update.save()

                # 삭제했으면 df_left에는 있고 df_right에는 없을 것이다.
                else:
                    row_to_delete = TestBulk.objects.get(pk=df_left.iloc[i, 0])
                    row_to_delete.delete()

            for i in range(0, len(df_right)):
                # df_left의 name column 내에 df_right의 i열 값이 들어가 있는가?
                is_same = df_left['name'] == df_right.iloc[i, 0]

                # 수정했으면 df_left에도 있을 것이고 df_right에도 있을 것이다.
                if is_same.sum() == 0:
                    # TeskBulk 모델 형태의 새로운 object 생성해준다.
                    row_to_plus = TestBulk()
                    # TeskBulk의 새로운 행에 데이터를 넣어준다.
                    row_to_plus.name=df_right.iloc[i, 0]
                    row_to_plus.address=df_right.iloc[i, 1]
                    row_to_plus.dept=df_right.iloc[i, 2]
                    row_to_plus.save()
                else:
                    is_same = 1

        elif action == 'action2': #추가 버튼 누를 경우: 실제로는 추가하기 위한 key값만 넘겨준다. 그리고 html에서 추가를 위한 입력란을 형성한다. 
            
            # 추가 버튼을 누르면, UI에 있는 input들을 일단은 임시저장 상태로 만들고 그걸 이용해 df를 만들어서 다시 뿌려준다.
            input_values_name = request.POST.getlist('name')
            input_values_address = request.POST.getlist('address')
            input_values_dept = request.POST.getlist('dept')
            
            result = zip(input_values_name, input_values_address, input_values_dept)

            for i, j, k in result:
                new_rows = [{'name':i, 'address':j, 'dept':k}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)
            
            context = {
                'list2' : df2,
                'action_key' : '추가'
            }

        elif action == 'action3': #등록 버튼 누를 경우: 추가했던 추가 칸이 합쳐진다.
            
            # 등록 버튼을 누르면 지금까지 수정, 추가했던 내용을 df2로 만들어주고 UI에 보낸다. 그러면 추가된 값도 input_values가 된다!
            input_values_name = request.POST.getlist('name')
            input_values_address = request.POST.getlist('address')
            input_values_dept = request.POST.getlist('dept')
            
            result = zip(input_values_name, input_values_address, input_values_dept)

            for i, j, k in result:
                new_rows = [{'name':i, 'address':j, 'dept':k}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)
            
            name_new = request.POST['name_new']
            address_new = request.POST['address_new']
            dept_new = request.POST['dept_new']

            if name_new == "none" : # name_new라는 것이 없을수도 있는데 없는대로 그냥 두면 multivaluerror 발생함. 따라서 none일 상황을 html에서 만들어준다.
                context = {
                'list2' : df2,
                'action_key' : '등록'
            }
            else : # name_new는 새로운 줄이다. 새로운 줄을 df2에 추가해준다.
                new_rows_new = [{'name': name_new, 'address': address_new, 'dept': dept_new}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows_new)], ignore_index=True)
                context = {
                'list2' : df2,
                'action_key' : '등록'
            }

        elif action == 'action4': #삭제 버튼을 누를 경우: df2에서 해당 선택한 라인을 지워주고 다시 보내준다.
            #multivalueDictkeyerror 해결방법
            if 'radio_name' in request.POST:
                del_target_name = request.POST["radio_name"] #삭제 버튼 누르면, 라디오 버튼의 선택값(radio_name, 즉 이름)을 넘겨받는다.
                
                # 일단 df2는 만들어주고, 그 후에 삭제 해당하는 것을 df2에서 없애주자.
                input_values_name = request.POST.getlist('name')
                input_values_address = request.POST.getlist('address')
                input_values_dept = request.POST.getlist('dept')
                
                result = zip(input_values_name, input_values_address, input_values_dept)

                for i, j, k in result:
                    new_rows = [{'name':i, 'address':j, 'dept':k}]
                    df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)
                
                # 삭제를 df2에서만 해준다.
                name_idx = df2[df2['name']==del_target_name].index
                df2 = df2.drop(name_idx)

                context = {
                    'list2' : df2,
                    'action_key' : '삭제'
                }
            else:
                context = {

                }

    return render(request, 'job2/test4.html', context)


def test5(request):

    models = TestBulk2.objects.all()

    context = {
        'database_values' : models,
        'key' : 'save'
    }

    return render(request, 'job2/test5.html', context)


def my_view(request): #test5의 다음단계

    action = request.POST['action']

    models = TestBulk2.objects.all()

    # df1이라는 dataframe을 만들기 위한 것임. 원래 DB와 같은 형태의 dataframe을 만들어서 사용함.
    original_rows=TestBulk2.objects.all()

    # data_list라는 리스트는 딕셔너리로 구성되어 있으며, 각 column name에 맞게 값들이 list화 되어있음.
    data_list = [{'dept_cd' : rows.dept_cd, 'name' : rows.name, 'pos': rows.pos} for rows in original_rows]

    # datalist 리스트를 이용해 dataframe df1생성. df1는 초기 DB값을 복사한 것이다.
    df1 = pd.DataFrame(data_list)
    df2 = pd.DataFrame()

    if request.method == 'POST':

        if action == 'action1': # 저장 버튼 누를 경우: 최종 결과값을 DB에 저장한다.
        #dataframe df2 초기 선언. df2는 UI의 최종 입력값이다.(추가 제외)
        
            # 입력값 저장 로직
            input1 = request.POST.getlist('input1')
            input2 = request.POST.getlist('input2')
            input3 = request.POST.getlist('input3')
            
            result = zip(input1, input2, input3)

            for i, j, k in result:
                new_rows = [{'dept_cd':i, 'name':j, 'pos':k}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)

            # df_left는 df1에는 있는데 df2에는 없는 것이다.(수정했거나 삭제한 것), df_right은 df2에는 있는데 df1에는 없는 것이다.(수정했거나 추가한 것)
            df_left = pd.merge(df1, df2, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge']).reset_index(drop=True)
            df_right = pd.merge(df1, df2, how='outer', indicator=True).query('_merge == "right_only"').drop(columns=['_merge']).reset_index(drop=True)

            print(df_left)
            print(df_right)
            # 먼저 df_left를 다룬다.
            for i in range(0, len(df_left)):
                # df_right의 name column 내에 df_left의 1열 값이 들어가 있는가? 를 확인하는 logic
                is_same = df_right['dept_cd'] == df_left.iloc[i, 0]

                # 수정했으면 df_left에도 있을 것이고 df_right에도 있을 것이다.
                if is_same.sum() > 0:
                    
                    #df1을 다룬다(DB쪽)
                    for j in range (1, len(df1.columns)):
                        column_name = df1.columns[j]

                        # df2의 해당되는 행의 값과 Testbulk(DB)를 비교해서 바뀐 것이 있으면 바꾼다. 열은 바뀌지 않는다.
                        # row_to_update는 TestBulk 테이블에서 pk값이 df_left즉 바뀌어야 하는 것만 빼놓은 df에서 i행 0열값, 즉 name과 같은 row가 row_to_update
                        row_to_update = TestBulk2.objects.get(pk=df_left.iloc[i,0])

                        #df2의 name값이 df_left.iloc[i,0](df_left는 수정해야되는 값만 있는 df지)인 행을 찾아서 그 행이 어딘지 알아냄.
                        n = int(df2[df2['dept_cd'] == df_left.iloc[i,0]].index[0])
                        
                        print(column_name)
                        print(n, j)
                        
                        #그래서 df2의 n행 j열 값을 알아내서 그걸 row_to_update에다가 넣을 것임
                        setattr(row_to_update, column_name, str(df2.iloc[n,j]))
                        row_to_update.save()

                # 삭제했으면 df_left에는 있고 df_right에는 없을 것이다.
                else:
                    row_to_delete = TestBulk2.objects.get(pk=df_left.iloc[i, 0])
                    row_to_delete.delete()

            # df_right을 다룬다.
            for i in range(0, len(df_right)):
                # df_left의 name column 내에 df_right의 i열 값이 들어가 있는가?
                is_same = df_left['dept_cd'] == df_right.iloc[i, 0]

                # 수정했으면 df_left에도 있을 것이고 df_right에도 있을 것이다.
                if is_same.sum() == 0: # 추가라면, is_same값은 0일 것이다. df_right 에만 있고 df_left에는 없는 것이다.
                    # TeskBulk 모델 형태의 새로운 row인 row_to_plus를 생성해준다.
                    row_to_plus = TestBulk2()
                    # TeskBulk의 새로운 행에 데이터를 넣어준다.
                    row_to_plus.dept_cd = df_right.iloc[i, 0]
                    row_to_plus.name = df_right.iloc[i, 1]
                    row_to_plus.pos = df_right.iloc[i, 2]
                    row_to_plus.save()
                else:
                    is_same = 1
        
            context = {
            'database_values' : models,
            'key' : 'save'
                } 

        elif action == 'action2': # 등록 버튼 누를 때

            # 등록 버튼을 누르면 지금까지 수정, 추가했던 내용을 df2로 만들어주고 UI에 보낸다. 그러면 추가된 값도 input_values가 된다!
            input1 = request.POST.getlist('input1')
            input2 = request.POST.getlist('input2')
            input3 = request.POST.getlist('input3')

            result = zip(input1, input2, input3)

            for i, j, k in result:
                new_rows = [{'dept_cd':i, 'name':j, 'pos':k}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)
        
                print(df2)

            context = {
                'database_values' : df2,
                'key' : 'register'
                #'action_key' : '등록'
            }
    
    return render(request, 'job2/test5.html', context)


def test6(request):

    models = TestBulk2.objects.all()

    context = {
        'database_values' : models,
        'key' : 'save'
    }

    return render(request, 'job2/test6.html', context)
    

def my_view_2(request): #test6의 다음단계, 새로운 방식의 update를 할 것임.

    action = request.POST['action']

    models = TestBulk2.objects.all()

    # df1이라는 dataframe을 만들기 위한 것임. 원래 DB와 같은 형태의 dataframe을 만들어서 사용함.
    original_rows=TestBulk2.objects.all()

    # data_list라는 리스트는 딕셔너리로 구성되어 있으며, 각 column name에 맞게 값들이 list화 되어있음.
    data_list = [{'dept_cd' : rows.dept_cd, 'name' : rows.name, 'pos': rows.pos} for rows in original_rows]

    # datalist 리스트를 이용해 dataframe df1생성. df1는 초기 DB값을 복사한 것이다.
    df1 = pd.DataFrame(data_list)
    df2 = pd.DataFrame()

    if request.method == 'POST':

        if action == 'action1': # 저장 버튼 누를 경우: 최종 결과값을 DB에 저장한다.
            
            #dataframe df2 초기 선언. df2는 UI의 최종 입력값이다.(추가 제외)
            # 입력값 저장 로직
            input1 = request.POST.getlist('input1')
            input2 = request.POST.getlist('input2')
            input3 = request.POST.getlist('input3')
            
            result = zip(input1, input2, input3)

            for i, j, k in result:
                new_rows = [{'dept_cd':i, 'name':j, 'pos':k}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)
        
            # # 데이터베이스의 모든 레코드를 가져옴
            # all_records = TestBulk2.objects.all()

            # # 데이터베이스의 레코드를 DataFrame으로 변환
            # df_database = pd.DataFrame.from_records(all_records.values())

            # # 추가된 행 찾기
            # df_added = pd.DataFrame(df2)
            # df_added = df_added[~df_added.isin(df_database)].dropna()

            # # 삭제된 행 찾기
            # df_deleted = df_database[~df_database.isin(df_added)].dropna()

            # # 추가된 행 생성
            # for index, added_row in df_added.iterrows():
            #     TestBulk2.objects.create(**added_row)

            # # 삭제된 행 삭제
            # for index, deleted_row in df_deleted.iterrows():
            #     record_to_delete = TestBulk2.objects.get(dept_cd=deleted_row['dept_cd'],
            #                                         name=deleted_row['name'],
            #                                         pos=deleted_row['pos'])
            #     record_to_delete.delete()

            # # 순회하면서 변경사항이 있는지 확인하고 업데이트
            # for modified_data in data_list_modified:
            #     # 데이터베이스에서 해당 레코드를 가져옴 (가정: prd_cd, dept_cd, job_cd가 고유한 키라고 가정)
            #     record_to_update = JobTask.objects.get(prd_cd=modified_data['prd_cd'],
            #                                dept_cd=modified_data['dept_cd'],
            #                                job_cd=modified_data['job_cd'])

            #     # 변경된 값을 데이터베이스 레코드에 적용
            #     record_to_update.duty_nm = modified_data['duty_nm']
            #     record_to_update.task_nm = modified_data['task_nm']
            #     record_to_update.task_prsn_chrg = modified_data['task_prsn_chrg']
            #     record_to_update.work_lv_sum = modified_data['work_lv_sum']

            #     # 변경사항을 저장
            #     record_to_update.save()

            context = {
            'database_values' : models,
            'key' : 'save'
            }

        elif action == 'action2': # 등록 버튼 누를 때

            # 등록 버튼을 누르면 지금까지 수정, 추가했던 내용을 df2로 만들어주고 UI에 보낸다. 그러면 추가된 값도 input_values가 된다!
            input1 = request.POST.getlist('input1')
            input2 = request.POST.getlist('input2')
            input3 = request.POST.getlist('input3')

            result = zip(input1, input2, input3)

            for i, j, k in result:
                new_rows = [{'dept_cd':i, 'name':j, 'pos':k}]
                df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)
        
                print(df2)

            context = {
                'database_values' : df2,
                'key' : 'register'
                #'action_key' : '등록'
            }
    
    return render(request, 'job2/test5.html', context)


def table(request):

    # 예시 데이터 생성
    data = {
        'group1': [0.1, 0.2, 0.3, 0.1],
        'group2': [0.15, 0.25, 0.35, 0.2],
        'group3': [0.1, 0.3, 0.4, 0.03],
        'group4': [0.1, None, 0.4, 0.2]
    }
    # df = pd.DataFrame(data, index=['Employee1', 'Employee2', 'Employee3', 'Employee4' ])
    df = pd.DataFrame(data)
    df['부서원'] = ['Employee1', 'Employee2', 'Employee3', 'Employee4']

    df = df[['부서원', 'group1', 'group2', 'group3', 'group4']]
    # df = df[['부서원']]
    # print(df)
    # 데이터프레임을 HTML 테이블 형태로 변환
    # html_table = df.to_html(classes='table')
    groups = ['group1', 'group2', 'group3' , 'group4']
    # groups = []
    df_json = df.to_json(orient='records')
    jobs_json = json.dumps(groups)  # jobs 리스트를 JSON으로 변환

    # contributions = {}
    # for employee in df.index:
    #     contributions[employee] = {}
    #     for job in df.columns:
    #         contributions[employee][job] = df.at[employee, job]

    # 템플릿에 전달할 컨텍스트 딕셔너리 생성
    context = {
        'df' : df,
        'data' : df_json,
        # 'jobs' : groups,
        'jobs_json' : jobs_json,

    }

    return render(request, 'job2/table.html', context)


# @csrf_exempt
# def update_dataframe(request):
#     if request.method == 'POST':
#         # 폼 데이터에서 입력 데이터 추출
#         data = request.POST

#         # 데이터를 처리하여 데이터베이스 업데이트 또는 다른 로직 수행
#         print(data)

#         return redirect('/success/')  # 처리 완료 후 다른 URL로 리다이렉트

#     return render(request, 'job2/table.html.html')


def submit_data(request):

    if request.method == 'POST':
        json_data = request.POST.get('jsonData')
        data = json.loads(json_data)
        df = pd.DataFrame(data)
        # DataFrame `df`를 사용하여 필요한 처리 수행

        columns = list(df.columns)

        columns.pop()
        columns.insert(0, 'employee')
        df.columns = columns

        # df의 마지막 행을 없애줌
        df = df[:-1]

        # df의 첫째 열을 제외하고 나머지 열들의 자료형을 float으로 바꿔줌
        for column in df.columns[1:]:
            # 해당 열 중에서 빈칸이 있으면 그 빈칸은 제외하고 float으로 바꿔줌
            df[column] = df[column].apply(lambda x: float(x) if x != '' else 0)

        # 나중에 DB에 저장할 때 0.0인 것은 저장하지 않을 것임.

        print(df)

        return render(request, 'job2/table.html')

    return render(request, 'job2/table.html')


def multiple(request):

    checked_data = ['선택1', '선택2']

    context = {
        'checked_data' : checked_data
    }

    if request.method == 'POST':

        check = request.POST.getlist('check')

        print(check)

        context = {
            'checked_data' : check
        }

    return render(request, 'job2/multiple.html', context)