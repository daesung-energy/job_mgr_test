let gridOptions = {
    columnDefs: [{
            // 그리드 헤더에 체크박스를 표시하는 옵션
            headerCheckboxSelection: true,
            // 각 행의 체크박스를 표시하는 옵션
            checkboxSelection: true,
            // 컬럼의 기본 너비
            width: 50,
            // 컬럼의 최소 너비
            minWidth: 50,
            // 컬럼의 최대 너비
            maxWidth: 100,
            // 그리드 스크롤이 수평으로 이동할 때 해당 컬럼을 고정하는 옵션
            pinned: 'left',
            // 그리드 상단에 부착되는 플로팅 필터를 허용하지 않도록 설정
            floatingFilter: false,
        },
        // 번호 컬럼
        // {
        //     headerName: '번호',
        //     valueGetter: 'node.rowIndex + 1',
        //     type: 'numericColumn',
        //     filter: 'agTextColumnFilter',
        //     width: 90,
        //     minWidth: 90,
        //     maxWidth: 150,
        //     valueParser: function (params) {
        //         // 입력된 값에서 숫자만 추출하여 반환
        //         return params.newValue.replace(/\D/g, '');
        //     },
        //     headerClass: 'numeric', // 타입에 따라 헤더에 클래스 추가
        // },
        // 나머지 데이터 컬럼
        // '회기' 컬럼 정의
        {
            headerName: '회기', // 헤더에 표시될 이름
            field: 'prd_cd', // 그리드에서 해당 컬럼에 매핑되는 데이터 필드
            type: 'text', // 컬럼의 데이터 타입 (여기서는 텍스트)
            filter: 'agTextColumnFilter', // 텍스트 필터 사용
            headerClass: 'text', // 헤더에 추가되는 클래스 (타입에 따라 헤더에 클래스 추가)
            width: 150, // 컬럼의 기본 너비
            minWidth: 120, // 컬럼의 최소 너비
            maxWidth: 150, // 컬럼의 최대 너비
            pinned: 'left', // 그리드에서 왼쪽에 고정
        },

        // '부서' 컬럼 정의
        {
            headerName: '부서',
            field: 'dept_cd',
            type: 'text',
            filter: 'agTextColumnFilter',
            headerClass: 'text',
            width: 150,
            minWidth: 120,
            maxWidth: 150,
            pinned: 'left',
        },

        // '직무코드' 컬럼 정의
        {
            headerName: '직무코드',
            field: 'job_cd',
            type: 'text',
            filter: 'agTextColumnFilter',
            // valueFormatter: dateFormatter, // 날짜 포맷을 변경하는 valueFormatter 사용
            headerClass: 'text',
            width: 150,
            minWidth: 120,
            maxWidth: 250,
        },

        // '책무' 컬럼 정의
        {
            headerName: '책무',
            field: 'task_nm',
            type: 'numeric',
            filter: 'agTextColumnFilter', 
            // valueFormatter: phoneFormatter, // 연락처 포맷을 변경하는 valueFormatter 사용
            headerClass: 'text',
            width: 150,
            minWidth: 120,
            maxWidth: 250,
            // valueParser: function (params) {
            //     // 입력된 값에서 숫자만 추출하여 반환
            //     return params.newValue.replace(/\D/g, '');
            // },
        },

        // '담당자' 컬럼 정의
        {
            headerName: '담당자',
            field: 'task_prsn_chrg',
            type: 'text',
            filter: 'agTextColumnFilter',
            headerClass: 'text',
            width: 150,
            minWidth: 120,
            maxWidth: 250,
        },

        // '업무수준' 컬럼 정의
        {
            headerName: '업무수준',
            field: 'work_lv_sum',
            type: 'numericColumn',
            filter: 'agTextColumnFilter', //타입은 numeric 이지만 필터는 Text로 필터링 
            // valueFormatter: commaFormatter, // 숫자를 쉼표 단위로 포맷하는 valueFormatter 사용
            headerClass: 'number',
            width: 150,
            minWidth: 120,
            maxWidth: 250,
            valueParser: function (params) {
                // 입력된 값에서 숫자만 추출하여 반환
                return params.newValue.replace(/\D/g, '');
            },
        },
    ],
    defaultColDef: {
        animateRows: true, // 행 애니메이션 활성화
        sortable: true, // 정렬 가능
        resizable: true, // 크기 조절 가능
        editable: true, // 편집 가능
        floatingFilter: true, // 플로팅 필터 사용
        filter: true, // 필터 사용
        cellClass: 'number-cell', // 각 셀에 적용할 클래스
    },
    floatingFiltersHeight: 30, // 플로팅 필터의 높이
    rowDragEntireRow: true, // 전체 행을 드래그할지 여부
    rowDragMultiRow: true, // 다중 행 드래그 허용 여부
    rowDragManaged: true, // 행 드래그를 그리드 외부에서 관리할지 여부
    rowSelection: 'multiple', // 다중 행 선택 모드
    suppressColumnMoveAnimation: true, // 열 이동 애니메이션 비활성화
    animateRows: true, // 행 추가 또는 삭제 애니메이션 적용
    getRowNodeId: data => data.번호, // 행 식별자 반환 함수
    onCellValueChanged: params => updateRowNumbers() // 셀 값 변경 이벤트 핸들러
};

/**
 * clearPinned 함수는 그리드에서 현재 고정된 열을 모두 해제하는 역할을 합니다.
 * gridApi를 활용하여 그리드에 적용할 열 상태를 설정하여 모든 열의 pinned 속성을 null로 설정합니다.
 * 
 * 1. gridApi를 사용하여 열 상태를 적용합니다.
 * 2. defaultState 객체 내부에서 pinned 속성을 null로 설정하여 모든 열의 고정을 해제합니다.
 * 
 * 이 함수를 호출하면 그리드에서 현재 고정된 열이 모두 해제되어 스크롤이 가능한 상태가 됩니다.
 */
function clearPinned() {
    // gridApi를 사용하여 그리드에 적용할 열 상태를 설정
    gridApi.applyColumnState({
        defaultState: {
            pinned: null // 모든 열의 pinned 속성을 null로 설정하여 고정 해제
        }
    });
}

/**
 * dateFormatter 함수는 날짜 데이터를 특정 형식(YYYY/MM/DD)으로 포맷팅하여 반환합니다.
 *
 * @param {Object} params - Ag-Grid 셀 렌더링에 사용되는 매개변수 객체
 * @param {any} params.value - 셀의 현재 값, 날짜 형식으로 전달됨
 *
 * 동작 설명:
 * 1. params 객체에서 날짜 값(params.value)을 가져와 새로운 Date 객체로 변환합니다.
 * 2. 연, 월, 일을 추출하여 각각의 값에 대해 필요한 포맷으로 조합합니다.
 * 3. 최종적으로 `${year}/${month}/${day}` 형식의 문자열로 반환합니다.
 * 4. 값이 없는 경우 빈 문자열('')을 반환합니다.
 *
 * 이 함수를 통해 숫자 형식의 날짜 데이터를 지정된 형식으로 변환하여 반환합니다.
 */
function dateFormatter(params) {
    // 날짜 값이 존재하는 경우
    if (params.value) {
        // Ag-Grid 셀 렌더링에 사용되는 날짜 값을 숫자에서 새로운 Date 객체로 변환
        let date = new Date(params.value.toString().replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3'));

        // 연도, 월, 일을 추출
        let year = date.getFullYear();
        let month = (date.getMonth() + 1).toString().padStart(2, '0');
        let day = date.getDate().toString().padStart(2, '0');

        // 'YYYY/MM/DD' 형식으로 문자열 반환
        return `${year}/${month}/${day}`;
    }

    // 값이 없는 경우 빈 문자열 반환
    return '';
}

/**
 * 전화번호 포맷터 함수
 * @param {object} params - Ag-Grid 셀 렌더링에 필요한 매개변수
 * @param {string|number} params.value - 셀에 저장된 값
 * @returns {string} - 포맷된 전화번호 문자열 또는 빈 문자열
 */
function phoneFormatter(params) {
    // 전화번호 값이 존재하는 경우
    if (params.value) {
        // 전화번호를 문자열로 변환
        let phoneNumber = params.value.toString();

        // 정규식을 사용하여 전화번호를 '000-0000-0000' 형식으로 포맷
        let formattedPhoneNumber = phoneNumber.replace(/(\d{3})(\d{4})(\d{4})/, '$1-$2-$3');

        // 포맷된 전화번호 문자열 반환
        return formattedPhoneNumber;
    }

    // 값이 없는 경우 빈 문자열 반환
    return '';
}

/**
 * 콤마 포맷터 함수
 * @param {object} params - Ag-Grid 셀 렌더링에 필요한 매개변수
 * @param {string|number} params.value - 셀에 저장된 값
 * @returns {string} - 콤마가 추가된 숫자 문자열 또는 빈 문자열
 */
function commaFormatter(params) {
    // 값이 존재하는 경우
    if (params.value) {
        // formatNumber 함수를 사용하여 콤마가 추가된 숫자 문자열 생성
        let formattedNumber = formatNumber(params.value);

        // 콤마가 추가된 숫자 문자열 반환
        return formattedNumber;
    }

    // 값이 없는 경우 빈 문자열 반환
    return '';
}

/**
 * 숫자 포맷터 함수
 * @param {number} number - 포맷할 숫자
 * @returns {string} - 콤마가 추가된 숫자 문자열
 */
function formatNumber(number) {
    // 주어진 숫자를 소수점 이하를 버리고 문자열로 변환한 뒤,
    // 정규 표현식을 사용하여 세 자리마다 콤마를 추가
    return Math.floor(number)
        .toString()
        .replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
}

/**
 * 텍스트 박스의 변경에 따라 그리드의 퀵 필터를 업데이트하는 함수
 */
function onFilterTextBoxChanged() {
    // 'filter-text-box'라는 ID를 가진 HTML 엘리먼트에서 값을 가져와서
    // 그리드 옵션의 API를 통해 퀵 필터를 설정
    gridOptions.api.setQuickFilter(
        document.getElementById('filter-text-box').value
    );
}

/**
 * 그리드의 렌더링된 노드들을 가져와서 번호를 업데이트하는 함수
 * @param {number} startIndex - 업데이트를 시작할 인덱스. 기본값은 0.
 */
function updateRowNumbers(startIndex = 0) {
    // 그리드 옵션에서 API를 통해 렌더링된 노드들을 가져옴
    let nodes = gridOptions.api.getRenderedNodes();

    // 가져온 노드들을 순회하면서 번호를 업데이트
    nodes.forEach((node, index) => {
        // 시작 인덱스 이상인 경우에만 번호 업데이트 수행
        if (index >= startIndex) {
            // 각 노드의 '번호' 필드에 인덱스 + 1 값을 설정
            node.setDataValue('번호', index + 1);
        }
    });
}

/**
 * 그리드에서 모든 행 선택을 해제하는 함수
 */
function deselect() {
    // 그리드 옵션에서 API를 통해 모든 행 선택 해제
    gridOptions.api.deselectAll();
}

/**
 * 선택된 행을 삭제하는 함수
 */
function deleteSelectedRows() {
    // 그리드에서 선택된 노드들을 가져옴
    let selectedNodes = gridOptions.api.getSelectedNodes();

    // 선택된 행이 하나 이상인 경우에만 처리
    if (selectedNodes.length > 0) {
        // 선택된 노드들에서 데이터를 추출하여 배열로 저장
        let selectedRows = selectedNodes.map(node => node.data);

        // 그리드 API를 사용하여 트랜잭션을 적용하여 행 삭제
        gridOptions.api.applyTransaction({
            remove: selectedRows
        });

        // 행 번호 업데이트
        updateRowNumbers();

        // 파일로 저장
        saveToFile();
    }
}

/**
 * 선택된 행 아래에 새로운 행을 추가하는 함수
 */
function addRowBelowSelected() {
    // 그리드에서 선택된 노드들을 가져옴
    let selectedNodes = gridOptions.api.getSelectedNodes();

    // 선택된 행이 하나 이상인 경우에만 처리
    if (selectedNodes.length > 0) {
        // 선택된 행 중 첫 번째 행의 인덱스를 가져옴
        let rowIndex = selectedNodes[0].rowIndex;

        // 새로운 데이터 객체 생성
        let newData = {
            회기: '',
            부서: '',
            직무코드: '',
            책무: '',
            담당자: '',
            업무수준: ''
        };

        // 그리드 API를 사용하여 트랜잭션을 적용하여 행 추가
        gridOptions.api.applyTransaction({
            add: [newData],
            addIndex: rowIndex + 1
        });

        // 행 번호 업데이트
        updateRowNumbers(rowIndex + 1);

        // 셀 강제 새로고침
        gridOptions.api.refreshCells({
            force: true
        });

        // 파일로 저장
        saveToFile();
    }
}

/**
 * 선택된 행을 복사하는 함수
 */
function copySelectedRows() {
    // 그리드에서 선택된 노드들을 가져옴
    let selectedNodes = gridOptions.api.getSelectedNodes();

    // 선택된 행이 하나 이상인 경우에만 처리
    if (selectedNodes.length > 0) {
        // 선택된 행들의 데이터를 복사하여 전역 변수인 'copiedRows'에 저장
        copiedRows = selectedNodes.map(node => ({
            ...node.data
        }));
    }
}

/**
 * 복사된 행을 선택된 행 아래에 붙여넣는 함수
 */
function pasteRows() {
    // 복사된 행이 존재하는 경우에만 처리
    if (copiedRows.length > 0) {
        // 그리드에서 선택된 노드들을 가져옴
        let selectedNodes = gridOptions.api.getSelectedNodes();

        // 붙여넣을 행의 인덱스 계산
        let rowIndex =
            selectedNodes.length > 0 ? selectedNodes[selectedNodes.length - 1].rowIndex + 1 : 0;

        // 'copiedRows'에 저장된 데이터를 그리드에 추가하되, 번호 필드는 변경하지 않음
        gridOptions.api.applyTransaction({
            add: copiedRows.map(row => ({
                ...row
            })),
            addIndex: rowIndex
        });

        // 행 번호 업데이트
        updateRowNumbers(rowIndex);

        // 그리드 셀 강제 갱신
        gridOptions.api.refreshCells({
            force: true
        });

        // 파일로 저장
        saveToFile();
    }
}

/**
 * 숫자 데이터를 CSV 파일로 저장할 때 금액 컬럼에서 쉼표(,)를 제외하고 저장하는 함수
 */
function saveToCSV() {
    // AG Grid에서 제공하는 API를 사용하여 현재 그리드의 데이터를 CSV 형식으로 내보냄
    gridOptions.api.exportDataAsCsv({
        // 저장될 파일의 이름 지정
        fileName: 'data.csv',
        // CSV 파일의 열 구분자로 콤마(,)를 사용
        columnSeparator: ',',
        // 데이터에 따옴표를 적용하지 않음
        suppressQuotes: false,
        // 데이터 포맷터를 사용하여 금액 컬럼에서 쉼표(,)를 제외하고 저장
        processCellCallback: function (params) {
            if (params.column.getColDef().field === '금액') {
                // 숫자에서 쉼표(,) 제거
                return params.value ? params.value.replace(/,/g, '') : params.value;
            }
            // 다른 컬럼은 그대로 반환
            return params.value;
        },
    });
}

/**
 * 그리드에 있는 데이터를 저장하는 함수
 */
function saveData() {
    // 버튼 텍스트 변경
    $("#saveData").text("save...");

    // 저장할 데이터를 담을 배열 초기화
    let saveList = [];

    // 그리드의 각 노드를 순회하며 데이터를 'saveList' 배열에 추가
    gridOptions.api.forEachNode((node, index) => {
        console.log(node);
        saveList.push(node.data);
    });

    // 콘솔에 저장된 데이터 출력
    console.log(saveList);
}

// 그리드를 인쇄하는 함수
function printGrid() {
    window.print();
}

/**
 * 그리드의 div 요소를 가져와서 해당 div에 대한 그리드를 생성하는 코드
 */
// HTML 문서에서 id가 'myGrid'인 요소를 가져옴
let eGridDiv = document.getElementById("myGrid");

// ag-Grid 라이브러리를 사용하여 그리드를 생성하고 'gridOptions' 설정을 적용
let grid = new agGrid.Grid(eGridDiv, gridOptions);

// 값이 없는 첫번째 행을 만들어 넣는다(입력 대기)
let newData = {
    회기: '',
    부서: '',
    직무코드: '',
    책무: '',
    담당자: '',
    업무수준: ''
};
gridOptions.api.applyTransaction({
    add: [newData],
    addIndex: 0
});

gridOptions.api.refreshCells({
    force: true
});

// =========================  ag-Grid 사용 안함 =============================

// 파일 입력(input) 요소에 이벤트 리스너 추가
// document.getElementById('fileInput').addEventListener('change', importCSV);

// 키 다운 이벤트에 대한 리스너 추가
// document.body.addEventListener('keydown', function (e) {
//     if (e.key === 'Escape') {
//         deselect();
//     }
// });

// /**
//  * CSV 파일을 가져와서 그리드에 적용하는 함수
//  * @param {Event} event - 파일 입력(input) 이벤트 객체
//  */
// function importCSV(event) {
//     // 파일 입력(input) 이벤트에서 파일 정보를 가져옴
//     let fileInput = event.target;
//     let file = fileInput.files[0];

//     // 파일이 존재하는 경우에만 처리
//     if (file) {
//         // Papa.parse 라이브러리를 사용하여 CSV 파일 파싱
//         Papa.parse(file, {
//             complete: function (result) {
//                 // CSV 파일의 첫 번째 행은 헤더로 사용
//                 let header = result.data[0];

//                 // 나머지 행은 데이터로 사용
//                 let data = result.data.slice(1);

//                 // 헤더와 데이터를 이용하여 그리드에 적용할 데이터로 가공
//                 for (let i = 0; i < data.length; i++) {
//                     let values = data[i];

//                     // 헤더와 데이터의 길이를 맞추기 위해 필요한 만큼 빈 값 추가
//                     let diff = header.length - values.length;
//                     if (diff > 0) {
//                         values.push(...Array(diff).fill(''));
//                     }

//                     // 헤더와 데이터를 쌍으로 하여 객체(row) 생성
//                     let row = {};
//                     for (let j = 0; j < header.length; j++) {
//                         row[header[j]] = values[j];
//                     }

//                     // 기존 데이터를 가공된 데이터로 교체
//                     data[i] = row;
//                 }

//                 // 그리드에 새로운 데이터 적용 및 행 번호 업데이트
//                 gridOptions.api.setRowData(data);
//                 updateRowNumbers();
//             }
//         });
//     }
// }

document.addEventListener('DOMContentLoaded', function() {
    var data = {{ data.values|safe }};
    
    var rowData = data;
    
    var gridDiv = document.querySelector('#myGrid');
    new agGrid.Grid(gridDiv, gridOptions);
});
