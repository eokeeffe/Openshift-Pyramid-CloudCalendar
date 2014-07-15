<%inherit file="pyramidapp:templates/layout.mak"/>

<div id="sse3">
    <div id="sses3">
        <ul>
            <li>
                <a href="${request.route_url('share_calendar',action='create')}">Share Calendar with another user</a>
            </li>
            <li>
                <a href="${request.route_url('revoke_calendar',action='create')}">Revoke sharing For a User</a>
            </li>
            <li>
                <a href="${request.route_url('home')}">Home</a>
            </li>
        </ul>
    </div>
</div>