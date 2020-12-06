import React, { useState, useEffect } from 'react';
import { AgGridColumn, AgGridReact } from 'ag-grid-react';
import axios from 'axios';

import { SERVER_BASE_URL } from '../../constants';

// AG Grid
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-balham-dark.css';

const priceFormatter = ({ value }) => `${(parseFloat(value).toFixed(2))}`;
const pctFormatter = ({ value }) => `${value > 0 ? '+' : ''}${(parseFloat(value).toFixed(2))}%`;
const numberFormatter = ({ value }) => `${value > 0 ? '+' : ''}${(parseFloat(value).toFixed(2))}`;
const volumeFormatter = ({ value }) => {
  if (value > 1e9) {
    return `${(parseFloat(value / 1e9).toFixed(2))} bn`
  } else {
    return `${(parseFloat(value / 1e6).toFixed(2))} mm`
  }
};

const numberCellStyle = threshold => params => {
  let degree = Math.min(Math.abs(params.value) / threshold, 1);
  if (params.value > 0) {
    return {
      backgroundColor: `rgb(0, ${degree * 64 + 144}, 0)`, color: '#fff'
    };
  } else if (params.value < 0) {
    return {
      backgroundColor: `rgb(${degree * 64 + 144}, 0, 0)`, color: '#fff'
    };
  } else {
    return {};
  }
};
const priceCellStyle = params => {
  var val = params.node.data.change;
  if (val > 0) {
    return { color: 'green', fontWeight: 'bold' };
  } else if (val < 0) {
    return { color: 'red', fontWeight: 'bold' };
  } else {
    return {};
  }
};

const StrongStocks = () => {
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
      const res = await axios.get(`${SERVER_BASE_URL}/strong_stocks`);
      setRowData(res.data);
    };
    fetchData();
  }, []);

  const defaultColDef = { sortable: true, filter: true, resizable: true };
  const columnTypes = {
    priceColumn: { valueFormatter: priceFormatter },
    pctColumn: { valueFormatter: pctFormatter },
    numberColumn: { valueFormatter: numberFormatter },
    volumeColume: { valueFormatter: volumeFormatter }
  };

  return (
    <div>
      <div className='ag-theme-balham-dark' style={{ width: '100%', height: 900 }}>
        <AgGridReact
          rowData={rowData}
          onGridReady={onGridReady}
          onFirstDataRendered={onFirstDataRendered}
          defaultColDef={defaultColDef}
          columnTypes={columnTypes}
        >
          <AgGridColumn field='id'></AgGridColumn>
          <AgGridColumn field='name'></AgGridColumn>
          <AgGridColumn field='price' cellStyle={priceCellStyle} headerName='Last Price'
            type={['priceColumn', 'rightAligned']}></AgGridColumn>
          <AgGridColumn field='changeRate' cellStyle={priceCellStyle} headerName='Change (%)'
            type={['pctColumn', 'rightAligned']}></AgGridColumn>
          <AgGridColumn field='change' cellStyle={priceCellStyle} headerName='Change'
            type={['numberColumn', 'rightAligned']}></AgGridColumn>
          <AgGridColumn field='rel1D' cellStyle={numberCellStyle(5)}
            type={['numberColumn', 'rightAligned']}></AgGridColumn>
          <AgGridColumn field='rel5D' cellStyle={numberCellStyle(20)}
            type={['numberColumn', 'rightAligned']}></AgGridColumn>
          <AgGridColumn field='rel20D' cellStyle={numberCellStyle(50)} type={['numberColumn', 'rightAligned']}></AgGridColumn>
          <AgGridColumn field='cs' cellStyle={numberCellStyle(15)} headerName='C/S'
            type={['numberColumn', 'rightAligned']}></AgGridColumn>
          <AgGridColumn field='sm' cellStyle={numberCellStyle(10)} headerName='S/M'
            type={['numberColumn', 'rightAligned']}></AgGridColumn>
          <AgGridColumn field='ml' cellStyle={numberCellStyle(8)} headerName='M/L'
            type={['numberColumn', 'rightAligned']}></AgGridColumn>
          <AgGridColumn field='volume' type={['volumeColume', 'rightAligned']}></AgGridColumn>
        </AgGridReact>
      </div>
      <br />
      <ul>
        <li>Rel1D: Price 1D Increase Rate - HSI 1D Increase Rate</li>
        <li>Rel5D: Price 5D Increase Rate - HSI 5D Increase Rate</li>
        <li>Rel10D: Price 20D Increase Rate - HSI 20D Increase Rate</li>
        <li>C/S : (Close - EMA20) / EMA20 * 100</li>
        <li>S/M : (EMA20 - EMA60) / EMA60 * 100</li>
        <li>M/L : (EMA60 - EMA120) / EMA120 * 100</li>
      </ul>
    </div>
  );
};

export default StrongStocks;