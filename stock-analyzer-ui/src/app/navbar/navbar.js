import React, { Component } from 'react';
import {
  MDBNavbar, MDBNavbarBrand, MDBNavbarNav, MDBNavItem, 
  MDBNavLink, MDBNavbarToggler, MDBCollapse
} from 'mdbreact';

class Navbar extends Component {
  state = {
    isOpen: false
  };

  toggleCollapse = () => {
    this.setState({ isOpen: !this.state.isOpen });
  }

  render() {
    return (
      <MDBNavbar color='grey darken-4' dark expand='md'>
        <MDBNavbarBrand>
          <strong className='white-text'>港股趋势分析</strong>
        </MDBNavbarBrand>
        <MDBNavbarToggler onClick={this.toggleCollapse} />
        <MDBCollapse id='navbarCollapse3' isOpen={this.state.isOpen} navbar>
          <MDBNavbarNav left>
            <MDBNavItem>
              <MDBNavLink to='/strong-stocks'>强势指标</MDBNavLink>
            </MDBNavItem>
            <MDBNavItem>
              <MDBNavLink to='/buy-sell-points'>买点卖点</MDBNavLink>
            </MDBNavItem>
            <MDBNavItem>
              <MDBNavLink to='/stock-view/0700.HK'>股票行情</MDBNavLink>
            </MDBNavItem>
          </MDBNavbarNav>
        </MDBCollapse>
      </MDBNavbar>
    );
  }
}

export default Navbar;