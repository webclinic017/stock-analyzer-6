import React from 'react';
import { useParams } from 'react-router-dom';
import StockChart from './stock-chart';

const StockView = () => {
  const { id } = useParams();
  return (
    < StockChart id={id} />
  );
}

export default StockView;