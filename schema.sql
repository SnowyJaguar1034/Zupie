CREATE TABLE IF NOT EXISTS public.guild
(
    guild_id bigint NOT NULL,
    premium boolean NOT NULL DEFAULT False,
    default_log_webhook text,
    has_guild_logs boolean NOT NULL DEFAULT False,
    guild_log_webhook text,
    has_member_logs boolean NOT NULL DEFAULT False,
    member_log_webhook text,
    has_messsage_logs boolean NOT NULL DEFAULT False,
    message_log_webhook text,
    has_role_logs boolean NOT NULL DEFAULT False,
    role_log_webhook text,
    has_channel_logs boolean NOT NULL DEFAULT False,
    channel_log_webhook text,
    has_voice_logs boolean NOT NULL DEFAULT False,
    voice_log_webhook text,
    has_join_leave_logs boolean NOT NULL DEFAULT False,
    join_leave_log_webhook text,
    has_mod_logs boolean NOT NULL DEFAULT False,
    mod_log_webhook text,
    has_raidmode_logs boolean NOT NULL DEFAULT False,
    raidmode_log_webhook text,
    has_raidmode_status boolean NOT NULL DEFAULT False,
    required_age smallint NOT NULL DEFAULT 7,
    has_greet_member boolean NOT NULL DEFAULT False,
    member_greetings text[],
    member_greeting_channel bigint,
    has_farewell_member boolean NOT NULL DEFAULT False,
    member_farewells text[],
    member_farewell_channel bigint,
    has_greet_bot boolean NOT NULL DEFAULT False,
    bot_greeting_channel bigint,
    has_farewell_bot boolean NOT NULL DEFAULT False,
    bot_farewell_channel bigint,
    has_bot_role boolean NOT NULL DEFAULT False,
    bot_role bigint,
    PRIMARY KEY (guild_id)
);

COMMENT ON TABLE public.guild
    IS 'The main table of Zupie, holds all Guild related Information.';

CREATE TABLE IF NOT EXISTS public.member
(
    member_id bigint,
    premium_slots smallint NOT NULL DEFAULT 0,
    "DM_Reminders" boolean NOT NULL DEFAULT False,
    PRIMARY KEY (member_id)
);

COMMENT ON TABLE public.member
    IS 'Holds member related information';

CREATE TABLE IF NOT EXISTS public.members_guilds
(
    member_id bigint,
    guild_id bigint,
    afk_status boolean NOT NULL DEFAULT False,
    afk_message text,
    joincount smallint NOT NULL DEFAULT 0,
    premium boolean NOT NULL DEFAULT False,
    PRIMARY KEY (member_id, guild_id)
);

COMMENT ON TABLE public.members_guilds
    IS 'Links the members table to the guilds table.';

CREATE TABLE IF NOT EXISTS public.reminders
(
    reminder_id bigserial NOT NULL,
    guild_id bigint,
    member_id bigint,
    reminder_time timestamp with time zone,
    reminder_text text,
    reminder_status boolean,
    PRIMARY KEY (reminder_id)
);

ALTER TABLE IF EXISTS public.guild
    ADD CONSTRAINT premium FOREIGN KEY (is_premium)
    REFERENCES public.members_guilds (premium) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.members_guilds
    ADD CONSTRAINT member_id FOREIGN KEY (member_id)
    REFERENCES public.member (member_id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.members_guilds
    ADD CONSTRAINT guild_id FOREIGN KEY (guild_id)
    REFERENCES public.guild (guild_id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.reminders
    ADD CONSTRAINT guild FOREIGN KEY (guild_id)
    REFERENCES public.guild (guild_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.reminders
    ADD CONSTRAINT "user" FOREIGN KEY (member_id)
    REFERENCES public.member (member_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;