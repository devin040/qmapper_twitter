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
  TopTrending,
  Betweeness,
  PageRank,
  PageRankWeight
} from './components';

import './style/App.css';

function App() {
  const [activeTab, setActiveTab] = useState('1');
  const [mActiveTab, setMActiveTab] = useState('1');

  const toggleTab = tab => {
    if(activeTab !== tab) setActiveTab(tab);
  }

  const toggleMetricTab = tab => {
    if(mActiveTab !== tab) setMActiveTab(tab);
  }

  return (
    <Container fluid id="container">
      <Row>
        <Col>
          <h1 className="text-center" id="tool-header">QAnon Network</h1>
        </Col>
      </Row>

      <Row>
        <Col sm="12" md="8">
          <Row>
            <Col>
              <Row>
                <Col>
                  <Vis />
                </Col>
              </Row>
              <Row>
                <Col>
                  <DegreeCharts />
                </Col>
              </Row>
            </Col>
          </Row>

          <Row className="mt-5">
            <Col>
              <Nav tabs>
                <NavItem>
                  <NavLink
                    className={classnames({ active: mActiveTab === '1' })}
                    onClick={() => { toggleMetricTab('1'); }}
                  >
                    Betweenness
                  </NavLink>
                </NavItem>
                <NavItem>
                  <NavLink
                    className={classnames({ active: mActiveTab === '2' })}
                    onClick={() => { toggleMetricTab('2'); }}
                  >
                    Page Rank
                  </NavLink>
                </NavItem>
                <NavItem>
                  <NavLink
                    className={classnames({ active: mActiveTab === '3' })}
                    onClick={() => { toggleMetricTab('3'); }}
                  >
                    Page Rank Weighted
                  </NavLink>
                </NavItem>
              </Nav>
              <TabContent activeTab={mActiveTab}>
                <TabPane tabId="1">
                  <Betweeness />
                </TabPane>
                <TabPane tabId="2">
                  <PageRank />
                </TabPane>
                <TabPane tabId="3">
                  <PageRankWeight />
                </TabPane>
              </TabContent>
            </Col>
          </Row>
        </Col>

        <Col sm="12" md="4">
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
    </Container>
  );
}

export default App;
