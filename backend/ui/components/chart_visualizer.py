"""
Chart Visualizer Component for MOSAIC

This module provides a UI component for visualizing chart data generated by the chart_data_generator agent.
It connects to the chart_data_generator agent to get data for various chart types and visualizes them using D3.js.
"""

import logging
import json
from typing import Dict, List, Any, Optional, Callable, Awaitable
from datetime import datetime

# Import the UI component base class
try:
    # Try importing with the full package path (for local development)
    from mosaic.backend.ui.base import UIComponent, ui_component_registry
    from mosaic.backend.agents.base import agent_registry
except ImportError:
    # Fall back to relative import (for Docker environment)
    from backend.ui.base import UIComponent, ui_component_registry
    from backend.agents.base import agent_registry

# Configure logging
logger = logging.getLogger("mosaic.ui.chart_visualizer")

class ChartVisualizerComponent(UIComponent):
    """
    Chart Visualizer Component for visualizing data from the chart_data_generator agent.
    
    This component provides:
    - Visualization of bar charts, line charts, pie charts, and scatter plots
    - Interactive controls for customizing chart parameters
    - Real-time data updates
    """
    
    def __init__(self):
        """Initialize the chart visualizer component."""
        super().__init__(
            component_id="chart-visualizer",
            name="Chart Visualizer",
            description="Component for visualizing data from the chart_data_generator agent",
            required_features=["visualization", "interactive"],
            default_modal_config={
                "title": "Chart Visualizer",
                "width": "80%",
                "height": "80%",
                "resizable": True
            }
        )
        
        # Register handlers
        self.register_handler("get_bar_chart_data", self.handle_get_bar_chart_data)
        self.register_handler("get_line_chart_data", self.handle_get_line_chart_data)
        self.register_handler("get_pie_chart_data", self.handle_get_pie_chart_data)
        self.register_handler("get_scatter_plot_data", self.handle_get_scatter_plot_data)
        self.register_handler("get_chart_data", self.handle_get_chart_data)
        
        logger.info(f"Initialized {self.name} component")
    
    async def handle_get_bar_chart_data(self, websocket: Any, event: Dict[str, Any], agent_id: str, client_id: str) -> None:
        """
        Handle a request to get bar chart data.
        
        Args:
            websocket: The WebSocket connection
            event: The event data
            agent_id: The agent ID
            client_id: The client ID
        """
        try:
            # Get parameters from the event data
            params = event.get("data", {})
            categories = params.get("categories")
            min_value = params.get("min_value", 0)
            max_value = params.get("max_value", 100)
            num_categories = params.get("num_categories", 5)
            
            logger.info(f"Getting bar chart data with {num_categories} categories")
            
            # Get the agent
            agent = await self._get_agent_runner()
            
            if not agent:
                raise ValueError(f"Agent {agent_id} not found")
            
            # Find the generate_bar_chart_data tool
            bar_chart_tool = None
            for tool in agent.tools:
                if tool.name == "generate_bar_chart_data":
                    bar_chart_tool = tool
                    break
            
            if not bar_chart_tool:
                raise ValueError("generate_bar_chart_data tool not found")
            
            # Call the generate_bar_chart_data tool directly
            result = bar_chart_tool.func(
                categories=categories,
                min_value=min_value,
                max_value=max_value,
                num_categories=num_categories
            )
            
            # Send the data back to the client
            await self._send_response(websocket, event, {
                "success": True,
                "chart_data": result
            })
        
        except Exception as e:
            logger.error(f"Error handling get bar chart data request: {str(e)}")
            
            # Send error response
            await self._send_response(websocket, event, {
                "success": False,
                "error": f"Error getting bar chart data: {str(e)}"
            })
    
    async def handle_get_line_chart_data(self, websocket: Any, event: Dict[str, Any], agent_id: str, client_id: str) -> None:
        """
        Handle a request to get line chart data.
        
        Args:
            websocket: The WebSocket connection
            event: The event data
            agent_id: The agent ID
            client_id: The client ID
        """
        try:
            # Get parameters from the event data
            params = event.get("data", {})
            points = params.get("points", 20)
            min_value = params.get("min_value", 0)
            max_value = params.get("max_value", 100)
            num_series = params.get("num_series", 1)
            series_names = params.get("series_names")
            
            logger.info(f"Getting line chart data with {points} points and {num_series} series")
            
            # Get the agent
            agent = await self._get_agent_runner()
            
            if not agent:
                raise ValueError(f"Agent {agent_id} not found")
            
            # Find the generate_line_chart_data tool
            line_chart_tool = None
            for tool in agent.tools:
                if tool.name == "generate_line_chart_data":
                    line_chart_tool = tool
                    break
            
            if not line_chart_tool:
                raise ValueError("generate_line_chart_data tool not found")
            
            # Call the generate_line_chart_data tool directly
            result = line_chart_tool.func(
                points=points,
                min_value=min_value,
                max_value=max_value,
                num_series=num_series,
                series_names=series_names
            )
            
            # Send the data back to the client
            await self._send_response(websocket, event, {
                "success": True,
                "chart_data": result
            })
        
        except Exception as e:
            logger.error(f"Error handling get line chart data request: {str(e)}")
            
            # Send error response
            await self._send_response(websocket, event, {
                "success": False,
                "error": f"Error getting line chart data: {str(e)}"
            })
    
    async def handle_get_pie_chart_data(self, websocket: Any, event: Dict[str, Any], agent_id: str, client_id: str) -> None:
        """
        Handle a request to get pie chart data.
        
        Args:
            websocket: The WebSocket connection
            event: The event data
            agent_id: The agent ID
            client_id: The client ID
        """
        try:
            # Get parameters from the event data
            params = event.get("data", {})
            segments = params.get("segments")
            min_value = params.get("min_value", 10)
            max_value = params.get("max_value", 100)
            num_segments = params.get("num_segments", 5)
            
            logger.info(f"Getting pie chart data with {num_segments} segments")
            
            # Get the agent
            agent = await self._get_agent_runner()
            
            if not agent:
                raise ValueError(f"Agent {agent_id} not found")
            
            # Find the generate_pie_chart_data tool
            pie_chart_tool = None
            for tool in agent.tools:
                if tool.name == "generate_pie_chart_data":
                    pie_chart_tool = tool
                    break
            
            if not pie_chart_tool:
                raise ValueError("generate_pie_chart_data tool not found")
            
            # Call the generate_pie_chart_data tool directly
            result = pie_chart_tool.func(
                segments=segments,
                min_value=min_value,
                max_value=max_value,
                num_segments=num_segments
            )
            
            # Send the data back to the client
            await self._send_response(websocket, event, {
                "success": True,
                "chart_data": result
            })
        
        except Exception as e:
            logger.error(f"Error handling get pie chart data request: {str(e)}")
            
            # Send error response
            await self._send_response(websocket, event, {
                "success": False,
                "error": f"Error getting pie chart data: {str(e)}"
            })
    
    async def handle_get_scatter_plot_data(self, websocket: Any, event: Dict[str, Any], agent_id: str, client_id: str) -> None:
        """
        Handle a request to get scatter plot data.
        
        Args:
            websocket: The WebSocket connection
            event: The event data
            agent_id: The agent ID
            client_id: The client ID
        """
        try:
            # Get parameters from the event data
            params = event.get("data", {})
            points = params.get("points", 50)
            x_min = params.get("x_min", 0)
            x_max = params.get("x_max", 100)
            y_min = params.get("y_min", 0)
            y_max = params.get("y_max", 100)
            num_series = params.get("num_series", 1)
            series_names = params.get("series_names")
            
            logger.info(f"Getting scatter plot data with {points} points and {num_series} series")
            
            # Get the agent
            agent = await self._get_agent_runner()
            
            if not agent:
                raise ValueError(f"Agent {agent_id} not found")
            
            # Find the generate_scatter_plot_data tool
            scatter_plot_tool = None
            for tool in agent.tools:
                if tool.name == "generate_scatter_plot_data":
                    scatter_plot_tool = tool
                    break
            
            if not scatter_plot_tool:
                raise ValueError("generate_scatter_plot_data tool not found")
            
            # Call the generate_scatter_plot_data tool directly
            result = scatter_plot_tool.func(
                points=points,
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                num_series=num_series,
                series_names=series_names
            )
            
            # Send the data back to the client
            await self._send_response(websocket, event, {
                "success": True,
                "chart_data": result
            })
        
        except Exception as e:
            logger.error(f"Error handling get scatter plot data request: {str(e)}")
            
            # Send error response
            await self._send_response(websocket, event, {
                "success": False,
                "error": f"Error getting scatter plot data: {str(e)}"
            })
    
    async def handle_get_chart_data(self, websocket: Any, event: Dict[str, Any], agent_id: str, client_id: str) -> None:
        """
        Handle a request to get chart data for any chart type.
        
        Args:
            websocket: The WebSocket connection
            event: The event data
            agent_id: The agent ID
            client_id: The client ID
        """
        try:
            # Get parameters from the event data
            params = event.get("data", {})
            chart_type = params.get("chart_type", "bar")
            
            # Call the appropriate handler based on the chart type
            if chart_type == "bar":
                await self.handle_get_bar_chart_data(websocket, event, agent_id, client_id)
            elif chart_type == "line":
                await self.handle_get_line_chart_data(websocket, event, agent_id, client_id)
            elif chart_type == "pie":
                await self.handle_get_pie_chart_data(websocket, event, agent_id, client_id)
            elif chart_type == "scatter":
                await self.handle_get_scatter_plot_data(websocket, event, agent_id, client_id)
            else:
                # Send error response for unsupported chart type
                await self._send_response(websocket, event, {
                    "success": False,
                    "error": f"Unsupported chart type: {chart_type}"
                })
        
        except Exception as e:
            logger.error(f"Error handling get chart data request: {str(e)}")
            
            # Send error response
            await self._send_response(websocket, event, {
                "success": False,
                "error": f"Error getting chart data: {str(e)}"
            })
    
    async def _get_agent_runner(self):
        """
        Get the agent runner.
        
        Returns:
            The agent runner
        """
        try:
            # Try importing with the full package path (for local development)
            from mosaic.backend.app.agent_runner import get_initialized_agents
        except ImportError:
            # Fall back to relative import (for Docker environment)
            from backend.app.agent_runner import get_initialized_agents
        
        # Get the initialized agents
        agents = get_initialized_agents()
        
        # Return the chart_data_generator agent
        return agents.get("chart_data_generator")
    
    async def _send_response(self, websocket: Any, event: Dict[str, Any], response_data: Dict[str, Any]) -> None:
        """
        Send a response back to the client.
        
        Args:
            websocket: The WebSocket connection
            event: The original event
            response_data: The response data
        """
        # Create the response event
        response = {
            "type": "ui_event",
            "data": {
                "component": self.component_id,
                "action": event.get("action", "unknown"),
                "requestId": event.get("requestId", "unknown"),
                **response_data
            }
        }
        
        # Send the response
        await websocket.send_json(response)

# Create and register the component
chart_visualizer_component = ChartVisualizerComponent()
ui_component_registry.register(chart_visualizer_component)

# Register the component with the chart_data_generator agent if it exists
if "chart_data_generator" in agent_registry.list_agents():
    agent_registry.register_ui_component("chart_data_generator", chart_visualizer_component.component_id)
    logger.info(f"Registered {chart_visualizer_component.name} component with chart_data_generator agent")
else:
    logger.info(f"Registered {chart_visualizer_component.name} component with ID {chart_visualizer_component.component_id}")
