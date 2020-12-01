import React, { useState } from 'react';
import { 
  Container, 
  Row, 
  Col,
  TabContent,
  TabPane,
  Nav,
  NavItem,
  NavLink
} from 'reactstrap';
import classnames from 'classnames'
import { 
  User, 
  Vis, 
  DegreeCharts,
  TopTrending
} from './components';

import './style/App.css';

function App() {
  const [activeTab, setActiveTab] = useState('1');

  const toggleTab = tab => {
    if(activeTab !== tab) setActiveTab(tab);
  }


  return (
    <Container fluid>
      <Row>
        <Col>
          <h1 className="text-center" id="tool-header">QAnon Network</h1>
        </Col>
      </Row>

      <Row>
        <Col sm="12" md="6">
          <Row>
            <Col>
              <Vis />
            </Col>
          </Row>
          <Row>
            <Col>
              <p>Average Degree Sample: 3.04</p>
              <p>Density: 0.06</p>
              <p>Diameter: 6</p>
            </Col>
          </Row>
        </Col>

        <Col sm="12" md="6">
          <Row>
            <Col>
              <User />
            </Col>
          </Row>

          <Row>
            <Col>
              <Nav tabs>
                <NavItem>
                  <NavLink
                    className={classnames({ active: activeTab === '1' })}
                    onClick={() => { toggleTab('1'); }}
                  >
                    Top Topics
                  </NavLink>
                </NavItem>
                <NavItem>
                  <NavLink
                    className={classnames({ active: activeTab === '2' })}
                    onClick={() => { toggleTab('2'); }}
                  >
                    Associated QDrops
                  </NavLink>
                </NavItem>
              </Nav>
              <TabContent activeTab={activeTab}>
                <TabPane tabId="1">
                  <Row>
                    <Col>
                      <TopTrending />
                    </Col>
                  </Row>
                </TabPane>
                <TabPane tabId="2">

                </TabPane>
              </TabContent>
            </Col>
          </Row>
        </Col>
      </Row>
      <DegreeCharts/>
    </Container>
  );
}

export default App;
