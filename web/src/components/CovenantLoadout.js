import React, { Component } from 'react';
import Tabs from './Tabs';
import covenantData from '../data/covenant-data.json';
import CovenantElement from "./CovenantElement";
import ConduitPicker from "./ConduitPicker";

export default class CovenantLoadout extends Component {

    constructor(props) {
        super(props);
        this.state = {
            currently_selected_covenant: -1,
            selected_covenant: [
                false, false, false, false
            ]
        }
    }

    covenantClickHandler = (name, idx) => {
        const selected_covenant = this.state.selected_covenant.slice();
        selected_covenant[this.state.currently_selected_covenant] = false;
        selected_covenant[idx] = true;

        this.setState({
            ...this.state,
            selected_covenant: selected_covenant,
            currently_selected_covenant: idx,
        });

        // pass changes to App
        this.props.covenantChangeHandler({name:name, idx: idx});
    };

    render() {
        // if covenant hasn't been selected yet - lock the other tab
        const noCovenantSelected = this.state.currently_selected_covenant === -1;

        return (
            <div className="covenantLoadoutContainer">
                <Tabs listId="covenant-tab-list">
                    <div label="Covenant">
                        <div className="flexLeft">
                            {covenantData["covenants"].map((covenant, idx) => (
                                <CovenantElement
                                    name={covenant.name}
                                    url={covenant.banner_url}
                                    index={idx}
                                    key={covenant.name + idx.toString()}
                                    clickHandler={this.covenantClickHandler}
                                    selected={this.state.selected_covenant[idx]}
                                    noneSelected={noCovenantSelected}
                                />
                            ))}
                        </div>
                    </div>
                    <div label="Conduits" locked={noCovenantSelected}>
                        <ConduitPicker
                            covenantId={this.state.currently_selected_covenant}
                        />
                    </div>
                </Tabs>
            </div>
        );
    }
}