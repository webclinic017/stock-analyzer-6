import { BrowserRouter as Router } from 'react-router-dom';

import Navbar from './navbar';
import Main from './main';

function App() {
  return (
    <Router>
      <Navbar />
      <Main />
    </Router>
  );
}

export default App;
