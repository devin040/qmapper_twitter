import React from 'react';
import { 
  Container, 
  Row, 
  Col
} from 'reactstrap';
import { User } from './components';

import './style/App.css';
import viz from './randomviz.png' 

function App() {
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
              <User />
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
