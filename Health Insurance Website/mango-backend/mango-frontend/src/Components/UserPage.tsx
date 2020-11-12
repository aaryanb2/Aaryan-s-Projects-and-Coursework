import React from 'react';
import {connect, ConnectedProps} from 'react-redux';
import {AppState, Entry, EntryType} from '../store/types';
import { 
  signIn as signInPredispatch,
  beginModifyEntry as beginModifyEntryPredispatch
} from '../store/actions';
import {
  Form, 
  Button, 
  Jumbotron, 
  Container, 
  Spinner, 
  FormControl,
  Tabs,
  Tab,
  Row,
  Col
} from 'react-bootstrap';
import './styles/UserPage.css'

const mapState = (state: AppState) => (
  {
    user: state.user,
    isSigningIn : state.isSigningIn,
    entries : state.userEntries
  }
)

const mapDispatch = {
  signIn : (user: string) => signInPredispatch(user),
  beginModifyEntry : (entryType: EntryType, index: number) => beginModifyEntryPredispatch(entryType, index)
}

const connector = connect(mapState, mapDispatch);

type UserPageProps = ConnectedProps<typeof connector>

interface UserPageState {
  userSignIn: string;
}

class UserPage extends React.Component<UserPageProps, UserPageState>{

  constructor(props : UserPageProps){
    super(props);

    this.state = {
      userSignIn : "",
    }
  }

  handleUserInput = (e: any) => {
    this.setState({userSignIn : e.target.value})
  }

  generateEntry = (entryType: EntryType, index : number, entry: Entry) => {
    return(
      <Row className={ entryType === EntryType.DRUG ? "drugentry" : "procentry" } key={index}>
        <Col> <span>{"Name: " + entry.name}</span> </Col>
        <Col> <span>{"Cost: " + entry.cost}</span> </Col>
        <Col> <span>{"With Insurance: " + entry.hasInsurance}</span></Col>
        <Col> <span>{"Zipcode: " + entry.zipcode}</span> </Col>
        <Col >
          <Button 
            variant='outline-primary' 
            onClick={() => this.props.beginModifyEntry(entryType, index)}
          >
            Edit
          </Button>
        </Col>
      </Row>
    )
  }

  render(){

    let {user, isSigningIn, entries, signIn} = this.props;
    let {userSignIn} = this.state;

    if(user === undefined){
      return (
        <div>
          <Container>
            <Jumbotron >
              <h1>Please Sign In</h1>
              <Form onSubmit={() => signIn(userSignIn)}>
                <FormControl onChange={this.handleUserInput}/>
                <Button disabled={userSignIn === ""} type="submit" >Sign In</Button>
              </Form>
              {
                isSigningIn && <Spinner animation="grow"/>
              }
            </Jumbotron>
          </Container>

        </div>
      )
    } else {
      return (
        <div className="user-entries" >
          <Container>
            <Tabs
              defaultActiveKey="drugs"
              id="entriestab"
            >
              <Tab eventKey="drugs" title="Drugs">
                <Container fluid>
                {
                  entries?.drugs.map( (drugEntry : any, index: number) => ( 
                    this.generateEntry(EntryType.DRUG, index, drugEntry)
                  ))
                }
                  <Row> 
                    <Col> 
                      <Button onClick={()=> this.props.beginModifyEntry(EntryType.DRUG, -1)}> 
                        + Insert New Drug 
                      </Button> 
                    </Col> 
                  </Row>
                </Container>
              </Tab>

              <Tab eventKey="procedures" title="Procedures">
                 <Container fluid>
                  {
                    entries?.procedures.map( (procEntry : any, index: number) => ( 
                      this.generateEntry(EntryType.PROCEDURE, index, procEntry)
                    ))
                  }
                  <Row> 
                    <Col> 
                      <Button onClick={() => this.props.beginModifyEntry(EntryType.PROCEDURE, -1)}>
                        + Insert New Procedure 
                      </Button> 
                    </Col> 
                  </Row>
                </Container>               
              </Tab>
            </Tabs>
          </Container>
        </div>
      )
    }
  }

}

export default connector(UserPage);