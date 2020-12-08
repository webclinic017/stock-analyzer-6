import React, { useState, useEffect } from 'react';
import { AgGridColumn, AgGridReact } from 'ag-grid-react';
import axios from 'axios';

import { SERVER_BASE_URL } from '../../constants';
import { numberFormatter, numberWithSignFormatter, pctWithSignFormatter, volumeFormatter, 
  priceAndChangeCellStyle, idCellRenderer } from '../../../common-grid/formatter';

// AG Grid
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-balham-dark.css';

const ma20SignCellStyle = ({ value }) => {
  const colorMap = {
    'TU': `rgb(0, 192, 0)`,
    'TD': `rgb(192, 0, 0)`
  };
  if (value !== '') {
    return {
      backgroundColor: colorMap[value], color: '#fff'
    };
  } else {
    return {};
  }
};

const biasPctCellStyle = ({ value }) => {
  const threshold = 0.9;
  if (value > threshold) {
    let degree = (value-threshold)/(1-threshold);
    return {
      backgroundColor: `rgb(${degree * 64 + 144}, 0, 0)`, color: '#fff'
    };
  } else {
    return {};
  }
};

const macdSignCellStyle = ({ value }) => {
  const colorMap = {
    'TU': `rgb(0, 192, 0)`, 'GC': `rgb(0, 224, 0)`,
    'TD': `rgb(192, 0, 0)`, 'DC': `rgb(224, 0, 0)`,
  }
  if (value !== '') {
    return {
      backgroundColor: colorMap[value], color: '#fff'
    };
  } else {
    return {};
  }
};

const kdjSignCellStyle = ({ value }) => {
  const colorMap = {
    'LGC': `rgb(0, 224, 0)`,
    'HDC': `rgb(224, 0, 0)`,
  }
  if (value !== '') {
    return {
      backgroundColor: colorMap[value], color: '#fff'
    };
  } else {
    return {};
  }
};

const segmentValueCellStyle = (upper, lower, range) => ({ value }) => {
  if (value > upper) {
    let degree = Math.min((value-upper)/range, 1);
    return {
      backgroundColor: `rgb(${degree * 64 + 144}, 0, 0)`, color: '#fff'
    };
  } else if (value < lower) {
    let degree = Math.min((lower-value)/range, 1);
    return {
      backgroundColor: `rgb(0, ${degree * 64 + 144}, 0)`, color: '#fff'
    };
  } else {
    return {};
  }
};

const upDownCellStyle = ({ value }) => {
  const colorMap = {
    'SU': `rgb(0, 224, 0)`,
    'DD': `rgb(224, 0, 0)`,
  }
  if (value !== '') {
    return {
      backgroundColor: colorMap[value], color: '#fff'
    };
  } else {
    return {};
  }
}


const BuySellPoints = () => {
  const [gridApi, setGridApi] = useState(null);
  const [rowData, setRowData] = useState([]);

  const onGridReady = ({ api }) => {
    setGridApi(api);
    const sortModel = [
      { colId: 'volume', sort: 'desc' }
    ];
    api.setSortModel(sortModel);
  };
  const sizeToFit = () => {
    if (gridApi) {
      gridApi.sizeColumnsToFit();
    }
  };

  // Auto fit size of columns when first time render data or window resized
  const onFirstDataRendered = ({ api }) => {
    api.sizeColumnsToFit();
  };
  useEffect(() => {
    window.addEventListener('resize', sizeToFit);
  });

  // Fetch strong stocks data
  useEffect(() => {
    const fetchData = async () => {
      const res = await axios.get(`${SERVER_BASE_URL}/buy_sell_points`);
      setRowData(res.data);
    };
    fetchData();
  }, []);

  const defaultColDef = { sortable: true, filter: true, resizable: true };

  return (
    <div>
      <div className='ag-theme-balham-dark' style={{ width: '100%', height: 900 }}>
        <AgGridReact
          rowData={rowData}
          onGridReady={onGridReady}
          onFirstDataRendered={onFirstDataRendered}
          defaultColDef={defaultColDef}
        >
          <AgGridColumn field='id' cellRenderer={idCellRenderer}></AgGridColumn>
          <AgGridColumn field='name'></AgGridColumn>
          <AgGridColumn field='price' cellStyle={priceAndChangeCellStyle} headerName='Last Price'
            type='rightAligned' valueFormatter={numberFormatter}></AgGridColumn>
          <AgGridColumn field='changeRate' cellStyle={priceAndChangeCellStyle} headerName='Change (%)'
            type='rightAligned' valueFormatter={pctWithSignFormatter}></AgGridColumn>
          <AgGridColumn field='bias' type='rightAligned' cellStyle={segmentValueCellStyle(15, -12, 15)} 
            valueFormatter={numberFormatter}></AgGridColumn>
          <AgGridColumn field='ma20' type='rightAligned' cellStyle={ma20SignCellStyle}></AgGridColumn>
          <AgGridColumn field='closeVsMa20' type='rightAligned' headerName='C. vs Ma20'
            cellStyle={upDownCellStyle}></AgGridColumn>
          <AgGridColumn field='biasPct' type='rightAligned' valueFormatter={numberFormatter}
            cellStyle={biasPctCellStyle}></AgGridColumn>
          <AgGridColumn field='bollRel1D' cellStyle={segmentValueCellStyle(0.9, -0.9, 0.3)} headerName='Boll Rel1D'
            type='rightAligned' valueFormatter={numberWithSignFormatter}></AgGridColumn>
          <AgGridColumn field='macd1D' type='rightAligned' cellStyle={macdSignCellStyle}></AgGridColumn>
          <AgGridColumn field='kdj1D' type='rightAligned' cellStyle={kdjSignCellStyle}></AgGridColumn>
          <AgGridColumn field='volume' type='rightAligned'
            valueFormatter={volumeFormatter}></AgGridColumn>
        </AgGridReact>
      </div>  
    </div>
  );
};

export default BuySellPoints;