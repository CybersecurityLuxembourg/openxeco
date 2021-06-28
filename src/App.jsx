import React from "react";
import "./App.css";
import "./css/medium-editor.css";
import { NotificationContainer, NotificationManager as nm } from "react-notifications";
import "react-notifications/lib/notifications.css";
import { BrowserRouter } from "react-router-dom";
import { withCookies } from "react-cookie";
import InsideApp from "./component/InsideApp.jsx";
import Login from "./component/Login.jsx";
import { getApiURL } from "./utils/env.jsx";
import { getRequest } from "./utils/request.jsx";

class App extends React.Component {
	constructor(props) {
		super(props);

		this.connect = this.connect.bind(this);
		this.getSettings = this.getSettings.bind(this);

		this.state = {
			settings: null,
			logged: false,
			email: null,
		};
	}

	// eslint-disable-next-line class-methods-use-this
	componentDidMount() {
		document.getElementById("favicon").href = getApiURL() + "public/get_image/favicon.ico";
		this.getSettings();
	}

	getSettings() {
		getRequest.call(this, "public/get_public_settings", (data) => {
			const settings = {};

			data.forEach((d) => {
				settings[d.property] = d.value;
			});

			this.setState({
				settings,
			});
		}, (response) => {
			nm.warning(response.statusText);
		}, (error) => {
			nm.error(error.message);
		});
	}

	connect(email) {
		this.setState({
			logged: true,
			email,
		});
	}

	render() {
		return (
			<div id="App">
				{this.state.logged
					? <BrowserRouter>
						<InsideApp
							email={this.state.email}
							cookies={this.props.cookies}
						/>
					</BrowserRouter>
					: <Login
						settings={this.state.settings}
						connect={this.connect}
						cookies={this.props.cookies}
					/>
				}
				<NotificationContainer/>
			</div>
		);
	}
}

export default withCookies(App);
