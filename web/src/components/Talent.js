import React, { Component } from 'react';

const getTalentStyle = selected => ({
    border: selected? '1px #fb1563 solid' : '',
    borderRadius: selected? '4px' : '',
    backgroundColor: selected? '#343f5e' : '#22293d',
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