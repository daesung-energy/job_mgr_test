//프린트
function printTableContent(tableId) {
    var table = document.getElementById(tableId);
    var tableTitle = document.querySelector('.' + tableId + '-title').innerText; // 테이블 제목 가져오기
    var content = '<h2>' + tableTitle + '</h2>' + table.outerHTML; // 테이블 제목과 표 전체의 HTML 코드를 가져옴
    var originalDocument = document.body.innerHTML;

    // 표의 내용을 현재 문서로 설정하여 프린트
    document.body.innerHTML = content;

    // 프린트 대화 상자 열기
    window.print();

    // 원래 문서로 복원
    document.body.innerHTML = originalDocument;
}


//-----------------엑셀로 저장-----------------
// 행사이즈 조절
function autoSizeColumns(worksheet) {

    //각 행 마다 가장 긴 글자 수를 기준으로 각 열 넓이 자동 조정
    worksheet.columns.forEach((column, columnIndex) => {
        let maxColumnLength = 0;
        column.eachCell({ includeEmpty: true }, cell => {
            const cellValue = cell.value ? cell.value.toString() : '';
            let cellLength = 0;

            // 각 문자에 대해 길이 측정
            for (let char of cellValue) {
                if (char.match(/[\uac00-\ud7a3]/)) { // 한글과 같은 폭이 넓은 문자 처리
                    cellLength += 2;
                } else if (char.match(/[\u0020-\u007E]/)) { // 기본 ASCII 문자
                    cellLength += 1;
                } else {
                    cellLength += 1.5; // 그 외 다른 문자 (일반적으로 넓은 문자)
                }
            }

            // 현재 셀의 길이가 저장된 최대 길이보다 크다면 업데이트
            if (cellLength * 2 > maxColumnLength) {
                maxColumnLength = cellLength * 2;
            }
            // 열의 너비를 최대 길이에 따라 설정, 최소 너비는 10으로 설정
            column.width = maxColumnLength < 10 ? 10 : maxColumnLength + 2; // 약간의 여유 공간 추가
        });
    });
}


// 버튼을 누를 경우 스타일 적용 후 Excel로 저장
function exportToExcel(tableId) {
    const fileName = prompt('파일 이름을 입력하세요.');
    if (fileName === null || fileName.trim() === '') {
        alert('파일 이름을 입력하세요.');
        return;
    }

    const table = document.getElementById(tableId);
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Sheet 1');

    // 검색 조건 라벨들을 HTML에서 동적으로 가져오기
    const criteriaIds = ['criteria1', 'criteria2', 'criteria3'];
    const searchCriteriaValues = criteriaIds.map(id => document.getElementById(id).value);
    const searchCriteriaLabels = criteriaIds.map(id => document.querySelector(`label[for="${id}"]`).textContent.replace(':', '').trim());

    // 드롭다운에서 선택된 검색 조건과 라벨을 첫 번째 행에 추가
    searchCriteriaLabels.forEach((label, index) => {
        const cellLabel = worksheet.getRow(1).getCell(index * 2 + 1);
        cellLabel.value = label;
        cellLabel.alignment = { horizontal: 'center' }; // 라벨 가운데 정렬
        cellLabel.font = { bold: true, size: 12 };

        const cellValue = worksheet.getRow(1).getCell(index * 2 + 2);
        cellValue.value = searchCriteriaValues[index];
        cellValue.alignment = { horizontal: 'center' }; // 값 가운데 정렬
        cellValue.font = { bold: false, size: 12 };
    });
    
    // 테이블 헤더를 두 번째 행에 저장하고 스타일 적용
    const headerRow = worksheet.getRow(3);
    table.querySelectorAll('th').forEach((th, index) => {
        const cell = headerRow.getCell(index + 1);
        cell.value = th.textContent;
        applyStylesToCell(cell, th);  // CSS 스타일 적용
    });

    // 테이블 데이터를 세 번째 행부터 저장하고 스타일 적용
    Array.from(table.querySelectorAll('tbody tr')).forEach((row, rowIndex) => {
        const dataRow = worksheet.getRow(rowIndex + 4);
        Array.from(row.cells).forEach((cell, cellIndex) => {
            const excelCell = dataRow.getCell(cellIndex + 1);
            excelCell.value = cell.textContent;
            applyStylesToCell(excelCell, cell);  // CSS 스타일 적용
        });
    });


    
    // 데이터 입력 완료 후, 열 넓이 자동 조정
    autoSizeColumns(worksheet);
    // 첫 번째 행의 높이를 20으로 설정
    worksheet.getRow(1).height = 20;


    // Excel 파일을 사용자에게 다운로드 제공
    workbook.xlsx.writeBuffer().then(function(buffer) {
        const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const url = window.URL.createObjectURL(blob);
        
        

        // 알림 창을 통해 파일 다운로드 제공
        const confirmation = confirm(`파일 이름: ${fileName}.xlsx \n파일을 다운로드하시겠습니까?`);
        if (confirmation) {
            const anchor = document.createElement('a');
            anchor.href = url;
            anchor.download = fileName + '.xlsx'; // 파일명에 사용자가 입력한 이름 추가
            anchor.click();
            window.URL.revokeObjectURL(url);
        }
    });
}
// 특정 HTML 요소에서 CSS 스타일을 읽어 Excel 셀에 적용하는 함수
function applyStylesToCell(excelCell, htmlElement) {
    const cssStyle = window.getComputedStyle(htmlElement);
    excelCell.style = {
        font: {
            bold: cssStyle.fontWeight === 'bold' || parseInt(cssStyle.fontWeight) > 400,
            color: { argb: colorToArgb(cssStyle.color) }
        },
        fill: {
            type: 'pattern',
            pattern: 'solid',
            fgColor: { argb: colorToArgb(cssStyle.backgroundColor) }
        },
        alignment: {
            horizontal: cssStyle.textAlign === 'right' ? 'right' : (cssStyle.textAlign === 'center' ? 'center' : 'left'),
            vertical: 'middle' // 수직 정렬 설정
        },
        border: {
            top: { style: 'thin', color: { argb: 'FF000000' } }, // 상단 테두리
            left: { style: 'thin', color: { argb: 'FF000000' } }, // 왼쪽 테두리
            bottom: { style: 'thin', color: { argb: 'FF000000' } }, // 하단 테두리
            right: { style: 'thin', color: { argb: 'FF000000' } }  // 오른쪽 테두리
        }
    };
}
// 색상 코드 변환 함수
function colorToArgb(color) {
    if (!color || color === 'rgba(0, 0, 0, 0)' || color === 'transparent') {
        return 'FFFFFFFF';  // 투명색 처리
    }
    const rgb = color.match(/\d+/g);
    return 'FF' + rgb.map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
}



//-----------------CSV로 저장-----------------

//CSV 파일로 저장
function downloadCSV(csvContent, fileName) {
    var csvBlob = new Blob(["\uFEFF" + csvContent], { type: 'text/csv;charset=utf-8;' });

    if (navigator.msSaveBlob) { // IE 및 Edge
        navigator.msSaveBlob(csvBlob, fileName);
    } else {
        // Anchor 엘리먼트를 생성하여 CSV 파일을 다운로드
        var link = document.createElement('a');
        link.href = URL.createObjectURL(csvBlob);
        link.download = fileName;
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

function convertToCSV(tableId) {
    var table = document.getElementById(tableId);
    var csv = [];

    // 테이블 제목 가져오기
    var tableTitle = document.querySelector('.' + tableId + '-title').innerText;
    //csv.push(tableTitle);

    // 테이블 헤더 가져오기
    var headers = [];
    for (var i = 0; i < table.rows[0].cells.length; i++) {
        headers[i] = table.rows[0].cells[i].innerText;
    }
    csv.push(headers.join(','));

    // 테이블 내용 가져오기
    for (var i = 1; i < table.rows.length; i++) {
        var row = [];
        for (var j = 0; j < table.rows[i].cells.length; j++) {
            row[j] = table.rows[i].cells[j].innerText;
        }
        csv.push(row.join(','));
    }

    var csvContent = csv.join('\n');
    console.log(csvContent);

    const fileName = prompt('파일 이름을 입력하세요.');
    if (fileName === null || fileName.trim() === '') {
        alert('파일 이름을 입력하세요.');
        return;
    }
    downloadCSV(csvContent, fileName);
}


