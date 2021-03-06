import React, { Component } from 'react';
import covenantData from '../data/covenant-data.json';
import conduitTree from '../data/conduit-tree.json';
import SoulbindElement from "./SoulbindElement";
import { Line } from 'react-lineto';
import ConduitElement from "./ConduitElement";
import CovenantPicker from "./CovenantPicker";

export default class CovenantLoadout extends Component {

    constructor(props) {
        super(props);
        this.doubleClickPrevention = true;
        this.state = {
            currently_selected_covenant: 0,
            currently_selected_soulbind: [
                0, 0, 0, 0
            ],
            selected_covenant: [
                true, false, false, false
            ],
            selected_soulbind: [
                [true, false, false],
                [true, false, false],
                [true, false, false],
                [true, false, false]
            ],
            selected_conduits: [
                false, false, false, false, false, false, false, false, false, false, false, false, false, false, false
            ],
            available_conduits: [
                false, false, false, false, false, false, false, false, false, false, false, false, false, false, false
            ],

        };
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

    conduitClickHandler = (name, idx, available, activating) => {
        // if the button is locked - do nothing
        if (!available) return;
        // this prevents double-click event when clicking on the 'x' component
        if (!this.doubleClickPrevention) {
            this.doubleClickPrevention = activating;
            return;
        }
        this.doubleClickPrevention = activating;

        // get correct collections within this nested awfulness
        const soulbinds = covenantData.covenants[this.state.currently_selected_covenant].soulbinds.slice();
        const selected_conduits = this.state.selected_conduits.slice();
        const available_conduits = this.state.available_conduits.slice();
        const tree_id =
            soulbinds[this.state.currently_selected_soulbind[this.state.currently_selected_covenant]].conduit_tree_id;

        const unlocks = conduitTree.tree_id[tree_id].conduits[idx].unlocks.slice();
        const locks = conduitTree.tree_id[tree_id].conduits[idx].locks.slice();

        // update which conduits are available/selected
        selected_conduits[idx] = activating;
        unlocks.map(e => {
            available_conduits[e] = activating;
        });
        locks.map(e => {
            available_conduits[e] = !activating;
        });
        this.setState({
            ...this.state,
            selected_conduits: selected_conduits,
            available_conduits: available_conduits
        });
    };

    soulbindClickHandler = (name, idx) => {
        const curr_soulbind_idx = this.state.currently_selected_soulbind[this.state.currently_selected_covenant];
        const soulbind_list = this.state.selected_soulbind.slice();
        const curr_selected_list = this.state.currently_selected_soulbind.slice();
        const _selected_soulbind = this.state.selected_soulbind[this.state.currently_selected_covenant].slice();
        _selected_soulbind[curr_soulbind_idx] = false;
        _selected_soulbind[idx] = true;

        soulbind_list[this.state.currently_selected_covenant] = _selected_soulbind;
        curr_selected_list[this.state.currently_selected_covenant] = idx;

        this.setState({
            ...this.state,
            currently_selected_soulbind: curr_selected_list,
            selected_soulbind: soulbind_list
        });

        // reset conduit trees
        for (let i = 0; i < this.state.selected_conduits.length; i++) {
            this.state.selected_conduits[i] = false;
        }
        for (let i = 0; i < this.state.available_conduits.length; i++) {
            this.state.available_conduits[i] = false;
        }
        //no need to pass anything to App
    };

    canBeUnselected = (unlocks) => {
        let unselectable = true;
        for (let i = 0; i < unlocks.length; i++) {
            unselectable = unselectable && !this.state.selected_conduits[unlocks[i]];
        }
        return unselectable;
    };

    render() {
        const offset = { x: 650, y: 660 };
        const soulbinds = covenantData.covenants[this.state.currently_selected_covenant].soulbinds.slice();
        const backgroundImage = ({
           background: 'url(' +
           soulbinds[this.state.currently_selected_soulbind[this.state.currently_selected_covenant]].background_img
           + ')'
        });
        const conduits =
            soulbinds[this.state.currently_selected_soulbind[this.state.currently_selected_covenant]].conduits.slice();
        const tree_id =
            soulbinds[this.state.currently_selected_soulbind[this.state.currently_selected_covenant]].conduit_tree_id;
        const lines = conduitTree.tree_id[tree_id].lines.slice();

        // set the first tree nodes as available
        const initAvailable = conduitTree.tree_id[tree_id].init_available;
        let hasInit = false;
        for (let i = 0; i < initAvailable.length; i++) {
            hasInit = hasInit || this.state.available_conduits[initAvailable[i]];
        }
        initAvailable.map(e => {
            if (!hasInit) {
                this.state.available_conduits[e] = true;
            }
        });

        return (
            <div className="conduitPickerContainer">
                <CovenantPicker
                    selectedCovenant={this.state.currently_selected_covenant}
                    clickHandler={this.covenantClickHandler}
                />

                <div className="flexLeft conduitsContainer" style={backgroundImage}>
                    <div className="flexDown">
                        {soulbinds.map((elem, idx) => (
                            <SoulbindElement
                                index={idx}
                                key={elem.name + idx.toString()}
                                name={elem.name}
                                url={elem.img_url}
                                selected={this.state.selected_soulbind[this.state.currently_selected_covenant][idx]}
                                clickHandler={this.soulbindClickHandler}
                                noneSelected={false}
                            />
                        ))}
                    </div>
                    <div>

                        {conduits.map((conduit, idx) => {
                            // get the coordinates for this conduit component
                            const coords = conduitTree.tree_id[tree_id].conduits[idx];
                            return (
                                <ConduitElement
                                    index={idx}
                                    key={conduit.name + idx.toString()}
                                    url={conduit.img}
                                    selected={this.state.selected_conduits[idx]}
                                    available={this.state.available_conduits[idx]}
                                    clickHandler={this.conduitClickHandler}
                                    coords_x={coords.x}
                                    coords_y={coords.y}
                                    spellId={conduit.spell_id}
                                    conduitType={conduit.type}
                                    canBeUnselected={this.canBeUnselected(coords.unlocks)}
                                />
                            )
                        })}

                        {lines.map((line, idx) => {
                            return (
                                <Line x0={line.x0 + offset.x} y0={line.y0 + offset.y}
                                      x1={line.x1 + offset.x} y1={line.y1 + offset.y}
                                      key={"line"+idx}
                                      className="conduitTreeLine"
                                      borderColor={this.state.selected_conduits[line.connects[0]] &&
                                        this.state.selected_conduits[line.connects[1]] ? "#00D97B" : '#6d778b'}
                                      borderWidth={8}
                                />
                            )
                        })}
                    </div>

                    <div className="conduitsRandomInfoBlock">
                        <div>
                            <h1 className="title">{soulbinds[this.state.currently_selected_soulbind[
                                this.state.currently_selected_covenant
                                ]].name}</h1>
                            <p className="infoParagraph">{soulbinds[this.state.currently_selected_soulbind[
                                this.state.currently_selected_covenant
                                ]].description}</p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}