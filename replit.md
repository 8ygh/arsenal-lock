# Overview

This is a ChatGPT-like Discord chatbot built with Python that uses Groq's lightning-fast AI models to provide intelligent, conversational responses. The bot can respond to direct messages, mentions, and slash commands, offering human-like conversations with ultra-fast response times.

# User Preferences

Preferred communication style: Simple, everyday language.
Request: Make it like ChatGPT using Groq for fast AI responses.
✅ **Implemented**: Bot now uses Groq's Llama-3.3-70B model for ChatGPT-like responses with lightning-fast inference.

# System Architecture

## Bot Framework
- **Discord.py Library**: Uses the discord.py library with the commands extension for bot functionality
- **Command Pattern**: Implements a command-based architecture with the `!` prefix for bot commands
- **Intents Configuration**: Configured with guild and member intents to access server and member information

## Configuration Management
- **Environment Variables**: Bot token is securely stored as an environment variable (`DISCORD_BOT_TOKEN`)
- **JSON Configuration**: Blacklisted servers are managed through a `blacklisted_servers.json` configuration file
- **File-based Storage**: Simple file-based approach for persistent configuration data

## Invite Processing System
- **Regex Pattern Matching**: Uses multiple regex patterns to extract Discord invite codes from various URL formats
- **URL Parsing**: Supports standard Discord invite formats including discord.gg, discord.com/invite, and discordapp.com/invite
- **Code Validation**: Validates both full invite URLs and standalone invite codes

## Error Handling
- **Configuration Validation**: Validates required environment variables on startup
- **File Management**: Handles missing configuration files by creating defaults
- **Graceful Degradation**: Implements fallback behaviors for missing or invalid configurations

# External Dependencies

## Core Dependencies
- **Discord.py**: Python library for Discord API integration
- **Python Standard Library**: Uses json, os, asyncio, re, and urllib.parse modules

## Discord API
- **Bot Permissions**: Requires guild and member access permissions
- **Invite Resolution**: Uses Discord's invite system to resolve server information

## Configuration Storage
- **Local File System**: Stores configuration in JSON format locally
- **Environment Variables**: Relies on system environment variables for sensitive data like bot tokens