import React from 'react';
import {AppState} from '../store/types';
import {connect, ConnectedProps} from 'react-redux'
import SearchPage from './SearchPage';
import UserPage from './UserPage';
import EntryEditor from './EntryEditor';

const mapState = (state: AppState) => (
  {
    page: state.page,
    isModifyingEntry: state.entryBeingModified
  }
)

const connector = connect(mapState);

type BodyProps = ConnectedProps<typeof connector>;

class Body extends React.Component<BodyProps>{

  render(){
    if(this.props.page === 0){
      return <SearchPage />
    }
    else if (this.props.page === 1){
      if(this.props.isModifyingEntry){
        return <EntryEditor />
      } else {
       return <UserPage />
      }
    }
  }
  
}

export default connector(Body);