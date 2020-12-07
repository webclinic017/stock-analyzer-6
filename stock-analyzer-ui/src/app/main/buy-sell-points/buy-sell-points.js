import React, { useState, useEffect } from 'react';
import { AgGridColumn, AgGridReact } from 'ag-grid-react';
import axios from 'axios';

import { SERVER_BASE_URL } from '../../constants';
import { numberFormatter, numberWithSignFormatter, pctWithSignFormatter, volumeFormatter, 
  priceAndChangeCellStyle, segmentColorCellStyle } from '../../../common-grid/formatter';

// AG Grid
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-balham-dark.css';


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

  console.log(rowData);

  return (
    <div>
      <div className='ag-theme-balham-dark' style={{ width: '100%', height: 900 }}>
        <AgGridReact
          rowData={rowData}
          onGridReady={onGridReady}
          onFirstDataRendered={onFirstDataRendered}
          defaultColDef={defaultColDef}
        >
          <AgGridColumn field='id'></AgGridColumn>
          <AgGridColumn field='name'></AgGridColumn>
          <AgGridColumn field='price' cellStyle={priceAndChangeCellStyle} headerName='Last Price'
            type='rightAligned' valueFormatter={numberFormatter}></AgGridColumn>
          <AgGridColumn field='changeRate' cellStyle={priceAndChangeCellStyle} headerName='Change (%)'
            type='rightAligned' valueFormatter={pctWithSignFormatter}></AgGridColumn>
          <AgGridColumn field='bollRel1D' cellStyle={segmentColorCellStyle(0.9, -0.9, 0.3)} headerName='Boll Rel1D'
            type='rightAligned' valueFormatter={numberWithSignFormatter}></AgGridColumn>
          <AgGridColumn field='volume' type='rightAligned'
            valueFormatter={volumeFormatter}></AgGridColumn>
        </AgGridReact>
      </div>
    </div>
  );
};

export default BuySellPoints;