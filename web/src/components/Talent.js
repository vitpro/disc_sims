import React, { Component } from 'react';

const getTalentStyle = selected => ({
    border: selected? '1px red solid' : '',
    borderRadius: selected? '3px' : '',
});

export default class Talent extends Component {

    render() {
        return (
            <div style={getTalentStyle(this.props.selected)} className="talentCell" onClick={() => this.props.talentClickHandler(this.props.index)}>
                <img src={this.props.url} className="talentCellImg"/>
                <span className="talentCellName">{this.props.name}</span>
            </div>
        );
    }
}