import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Row, 
  Col, 
  Table, 
  Dropdown, 
  DropdownToggle, 
  DropdownMenu, 
  DropdownItem 
} from 'reactstrap';

import apiWrapper from './api'
import './style/App.css';
import viz from './randomviz.png' 

function App() {
  const [dropdownOpen, setDropdownOpen] = useState(false);

  useEffect(() => {
    async function fetchData() {
      let testResult = await apiWrapper.testMethod();
      console.log(testResult.data); 
    }
    fetchData();
  })

  const toggle = () => setDropdownOpen(prevState => !prevState);

  return (
    <Container fluid>
      <Row>
        <Col>
          <h1 className="text-center" id="tool-header">QAnon Network</h1>
        </Col>
      </Row>

      <Row>
        <Col sm="12" md="4">
          <p>Average Degree Sample: 3.04</p>
          <p>Density: 0.06</p>
          <p>Diameter: 6</p>
        </Col>

        <Col sm="12" md="4">
          <img src={viz} alt="random viz"/>
        </Col>

        <Col sm="12" md="4">
          <Row>
            <Col>
              <Table bordered>
                <thead>
                  <tr>
                    <th>Top Users</th>
                    <th>
                      <Dropdown isOpen={dropdownOpen} toggle={toggle}>
                        <DropdownToggle caret>
                          Filter
                        </DropdownToggle>
                        <DropdownMenu>
                          <DropdownItem>Filter 1</DropdownItem>
                        </DropdownMenu>
                      </Dropdown>
                    </th>
                  </tr>
                </thead>

                <tbody>
                  <tr>
                    <td>User 1</td>
                    <td>User 2</td>
                  </tr>
                </tbody>
              </Table>
            </Col>
          </Row>

          <Row>
            <Col sm="12" md="6">
              <h2>Trending Topics</h2>
              <p>#Topic1</p>
              <p>#Topic2</p>
            </Col>
            <Col sm="12" md="6">
              <h2>QAnon Trending Topics</h2>
              <p>#Topic1</p>
              <p>#Topic2</p>
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
