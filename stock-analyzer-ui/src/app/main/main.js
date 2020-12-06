import React from 'react';

import { Switch, Route } from 'react-router-dom';
import StrongStocks from './strong-stocks';

const Main = () => (
  <main className='p-3'>
    <Switch>
      <Route path='/strong-stocks'>
        <StrongStocks />
      </Route>
      <Route path='/'>
        <StrongStocks />
      </Route>
    </Switch>
  </main>
);

export default Main;