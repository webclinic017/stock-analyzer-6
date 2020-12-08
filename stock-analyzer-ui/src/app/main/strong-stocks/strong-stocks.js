import React, { useState, useEffect } from 'react';
import { AgGridColumn, AgGridReact } from 'ag-grid-react';
import axios from 'axios';

import { SERVER_BASE_URL } from '../../constants';
import { numberFormatter, numberWithSignFormatter, pctWithSignFormatter, volumeFormatter, idCellRenderer,
  priceAndChangeCellStyle, bgGreenRedColorMapCellStyle } from '../../../common-grid/formatter';

// AG Grid
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-balham-dark.css';

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
          <AgGridColumn field='change' cellStyle={priceAndChangeCellStyle} headerName='Change'
            type='rightAligned' valueFormatter={numberWithSignFormatter}></AgGridColumn>
          <AgGridColumn field='rel1D' cellStyle={bgGreenRedColorMapCellStyle(5)}
            type='rightAligned' valueFormatter={numberWithSignFormatter}></AgGridColumn>
          <AgGridColumn field='rel5D' cellStyle={bgGreenRedColorMapCellStyle(20)}
            type='rightAligned' valueFormatter={numberWithSignFormatter}></AgGridColumn>
          <AgGridColumn field='rel20D' cellStyle={bgGreenRedColorMapCellStyle(50)}
            type='rightAligned' valueFormatter={numberWithSignFormatter}></AgGridColumn>
          <AgGridColumn field='cs' cellStyle={bgGreenRedColorMapCellStyle(15)} headerName='C/S'
            type='rightAligned' valueFormatter={numberWithSignFormatter}></AgGridColumn>
          <AgGridColumn field='sm' cellStyle={bgGreenRedColorMapCellStyle(10)} headerName='S/M'
            type='rightAligned' valueFormatter={numberWithSignFormatter}></AgGridColumn>
          <AgGridColumn field='ml' cellStyle={bgGreenRedColorMapCellStyle(8)} headerName='M/L'
            type='rightAligned' valueFormatter={numberWithSignFormatter}></AgGridColumn>
          <AgGridColumn field='volume' type='rightAligned'
            valueFormatter={volumeFormatter}></AgGridColumn>
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