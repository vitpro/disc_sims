import React, { Component } from 'react';
import Tabs from './Tabs';
import raceData from '../data/race-data.json';
import RaceElement from "./RaceElement";

export default class RacePicker extends Component {

    constructor(props) {
        super(props);
        this.state = {
            currently_selected_horde: -1,
            currently_selected_alliance: -1,
            selected_race_horde: [
                false, false, false, false, false, false,
                false, false, false, false, false, false,
            ],
            selected_race_alliance: [
                false, false, false, false, false, false,
                false, false, false, false, false, false,
            ]
        };
    }

    hordeRaceClickHandler = (name, idx) => {
        const selected_race = this.state.selected_race_horde.slice();
        selected_race[this.state.currently_selected_horde] = false;
        selected_race[idx] = true;

        this.setState({
            ...this.state,
            selected_race_horde: selected_race,
            currently_selected_horde: idx,
        });

        this.props.raceChangeHandler(name);
    };

    allianceRaceClickHandler = (name, idx) => {
        const selected_race = this.state.selected_race_alliance.slice();
        selected_race[this.state.currently_selected_alliance] = false;
        selected_race[idx] = true;

        this.setState({
            ...this.state,
            selected_race_alliance: selected_race,
            currently_selected_alliance: idx,
        });

        this.props.raceChangeHandler(name);
    };

    render() {
        const allianceNoneSelected = this.state.currently_selected_alliance === -1;
        const hordeNoneSelected = this.state.currently_selected_horde === -1;

        return (
            <div className="racePickerGrid">
               <Tabs listId="race-picker-tab-list">
                   <div label="Horde">
                       <div className="raceIconsContainer">
                           {raceData["horde"].map((race, idx) => (
                               <RaceElement
                                   index={idx}
                                   key={race.name + idx.toString()}
                                   name={race.name}
                                   url={race.url}
                                   selected={this.state.selected_race_horde[idx]}
                                   clickHandler={this.hordeRaceClickHandler}
                                   noneSelected={hordeNoneSelected}
                               />
                           ))}
                       </div>
                   </div>
                   <div label="Alliance">
                       <div className="raceIconsContainer">
                           {raceData["alliance"].map((race, idx) => (
                               <RaceElement
                                   index={idx}
                                   key={race.name + idx.toString()}
                                   name={race.name}
                                   url={race.url}
                                   selected={this.state.selected_race_alliance[idx]}
                                   clickHandler={this.allianceRaceClickHandler}
                                   noneSelected={allianceNoneSelected}
                               />
                           ))}
                       </div>
                   </div>
               </Tabs>
            </div>
        );
    }
}