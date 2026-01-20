"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { ResponsiveContainer, Tooltip, Cell, Pie, PieChart, Bar, BarChart, XAxis, YAxis, CartesianGrid, Radar, RadarChart, PolarGrid, PolarAngleAxis, Line, LineChart } from "recharts";
import { useRouter } from "next/navigation";
import Link from "next/link";
import RandomColor from "../components/RandomColor";

type FavoriteTypes = {
    id: number;
    label: string;
};

type PlaystyleStats = {
  primary: string;
  scores: Record<string, number>;
};

type GenreVariety = {
  unique_genres: number;
  total_games: number;
  index: number;
};

type ProfileStatisticsTypes = {
    total_games: number;
    completed_games: number;
    playing_games: number;
    backlog_games: number;
    dropped_games: number;
    paused_games: number;
    total_playtime: number;
    yearly_completed_games: Record<string, number>;
    favorite_developers: FavoriteTypes[];
    favorite_publishers: FavoriteTypes[];
    favorite_genres: FavoriteTypes[];
    favorite_platforms: FavoriteTypes[];
    favorite_franchises: FavoriteTypes[];
    favorite_series: FavoriteTypes[];
    playstyle: PlaystyleStats;
    commitment_chart: Record<string, number>;
    genre_variety: GenreVariety;
    dropoff_depth: number;
};

type FavoriteGameTypes = {
    id: number;
    igdb_id: number;
    game_title: string;
    cover_artwork_link: string | null;
};

type LogType = {
    game: {
        id: number;
        igdb_id: number;
        game_title: string;
        cover_artwork_link: string | null;
    };
    user_playtime: number;
    user_status: string;
    user_rating: number;
    start_date: string;
    completion_date: string | null;
    full_completion: boolean | null;
};

type ProfileTypes = {
    username: string;
    bio: string;
    private_profile: boolean;
    profile_photo: string | null;
    favorite_game: FavoriteGameTypes | null,
    statistics: ProfileStatisticsTypes | null;
    logs?: LogType[];
};

const Profile = () => {
    const router = useRouter();
    const [profile, setProfile] = useState<ProfileTypes>({
        username: "",
        bio: "",
        private_profile: false,
        profile_photo: null,
        favorite_game: null,
        statistics: null,
    });
    useEffect(() => {
        const token = localStorage.getItem("access");
        if (!token) {
            router.push("/not-found");
            return;
        }
        const fetchProfile = async () => {
            const authentication = await apiFetch("/authentication/profile/");
            const personal = await apiFetch("/profiles/personal/");
            setProfile({
                username: authentication.username,
                bio: personal?.bio ?? "",
                private_profile: personal?.private_profile ?? false,
                profile_photo: personal?.profile_photo ?? null,
                favorite_game: personal?.favorite_game ?? null,
                statistics: personal?.statistics ?? null,
                logs: personal?.logs ?? [],
            });
        };
        fetchProfile();
    }, []);
    const favoriteGameLog = profile.favorite_game ? (profile.logs ?? []).find(log => log.game.id === profile.favorite_game!.igdb_id) : null;
    const statusData = profile.statistics ? [{name: "Completed", value: profile.statistics.completed_games}, {name: "Playing", value: profile.statistics.playing_games}, {name: "Backlog", value: profile.statistics.backlog_games}, {name: "Dropped", value: profile.statistics.dropped_games}, {name: "Paused", value: profile.statistics.paused_games},] : [];
    const statisticColors = ["#EC4E20", "#FF9505", "#FC60A8", "#65DD65", "#5466EB"];
    const completionRate = profile.statistics ? Math.round((profile.statistics.completed_games / Math.max(profile.statistics.total_games, 1)) * 100) : 0;
    const playstyleRadarData = profile.statistics ? Object.entries(profile.statistics.playstyle.scores).map(([key, value]) => ({metric: key.replace("_", " "),value,})) : [];
    const radarColor = statisticColors[playstyleRadarData.length % statisticColors.length];
    const commitmentData = profile.statistics ? Object.entries(profile.statistics.commitment_chart).map(([label, count]) => ({label, count,})) : [];
    const commitmentColor = statisticColors[commitmentData.length % statisticColors.length];
    const now = new Date();
    const lastFiveYears = profile.statistics ? Object.entries(profile.statistics.yearly_completed_games)
        .filter(([yearStr, _]) => {
            const year = parseInt(yearStr);
            return year >= now.getFullYear() - 4;
        })
        .map(([year, count]) => ({year, count})) : [];
    const oneYearAgo = new Date(); oneYearAgo.setFullYear(now.getFullYear() - 1);
    const timelineData = (profile.logs ?? []).filter(log => log.start_date).map(log => ({gameTitle: profile.favorite_game?.game_title ?? "Unknown", y: log.user_playtime ?? 0, start: new Date(log.start_date).getTime(), end: log.completion_date ? new Date(log.completion_date).getTime() : null,})).filter(log => log.start >= oneYearAgo.getTime());
    const SectionHeader = ({title}: {title: string}) => (
        <>
            <RandomColor constant><h1 className = "text-xl font-main-title">{title}</h1></RandomColor>
            <p className = "break-up-line"></p>
        </>
    );
    const StatCard = ({title, value}: {title: string; value: string | number}) => (
        <div className = "bg-ui rounded-lg p-4 outline-4 outline-white text-center">
            <RandomColor constant><h1 className = "text-xl font-main-title">{title}</h1></RandomColor>
            <p className = "text-3xl mt-2">{value}</p>
        </div>
    );
    const DataNotAvailable = ({text = "No data available yet"}) => (
        <div className="flex items-center justify-center h-75 opacity-60 text-xl">{text}</div>
    );
    const CustomTooltip = ({ active, payload, label }: any) => {
        if (active && payload && payload.length) {
            return (
                <div className = "bg-ui p-2 rounded-lg outline-4 outline-white shadow-md">
                    {label && <p className = "font-main-title">{label}</p>}
                    {payload.map((entry: any, idx: number) => (<p key = {idx} className = "text-xl">{entry.name}: {entry.value}</p>))}
                </div>
            );
        }
        return null;
    };
    if (!profile) {
        return <h1>Loading...</h1>
    }
    else {
        return (
            <div className = "base-background pl-5 pr-5 pt-20 overflow-x-hidden">
                <div className = "grid grid-cols-[250px_1fr]">
                    <div className = "space-y-6 items-center flex flex-col">
                        <RandomColor constant><h1 className="text-3xl font-main-title">{profile.username}</h1></RandomColor>
                        {profile.profile_photo && (<img src = {profile.profile_photo} alt = "Profile Photo" className = "w-48 h-48 rounded-full outline-4 outline-white object-cover" />)}
                        <RandomColor element = "bg"><button onClick={() => router.push("/profile/edit")} className = "btn bg-ui mt-4">Edit Profile</button></RandomColor>
                    </div>
                    <div className = "space-y-4">
                        <SectionHeader title = "Bio" /><p className = "indent-5 text-xl">{profile.bio || "No bio provided..."}</p>
                        <p className = "break-up-line mb-10"></p>
                        {profile.favorite_game && (
                            <>
                                <SectionHeader title = "Favorite Game" />
                                <RandomColor element = "bg">
                                    <Link href = {`/games/${profile.favorite_game.igdb_id}`} className = "p-4 bg-ui rounded-lg outline-4 outline-white flex items-center gap-5 transition">
                                        {profile.favorite_game.cover_artwork_link ? (
                                            <img src = {profile.favorite_game.cover_artwork_link} alt = {profile.favorite_game.game_title} className="w-50 rounded-lg outline-4 outline-white" />
                                        ) : (
                                            <img src = "/images/missing.jpg" alt = "Missing" className = "w-50 rounded-lg outline-4 outline-white" />
                                        )}
                                        <div className = "flex-1">
                                            <p className = "text-3xl font-main-title mb-3">{profile.favorite_game.game_title}</p>
                                            <div className = "grid grid-cols-3 gap-x-8 gap-y-4 ml-10">
                                                <div className = "space-y-3">
                                                    <h1 className = "text-2xl font-main-title">Status:</h1>
                                                    <p className = "indent-5 text-xl">{favoriteGameLog?.user_status}</p>
                                                    {favoriteGameLog?.user_rating !== null && (
                                                        <>
                                                            <h1 className = "text-2xl font-main-title">Rating:</h1>
                                                            <p className = "indent-5 text-xl">{favoriteGameLog?.user_rating}/10</p>
                                                        </>
                                                    )}
                                                    {favoriteGameLog?.user_playtime !== null && (
                                                        <>
                                                            <h1 className = "text-2xl font-main-title">Playtime:</h1>
                                                            <p className = "indent-5 text-xl">{favoriteGameLog?.user_playtime} Hours</p>
                                                        </>
                                                    )}
                                                </div>
                                                <div className = "space-y-3">
                                                    {favoriteGameLog?.start_date && (
                                                        <>
                                                            <h1 className = "text-2xl font-main-title">Start Date:</h1>
                                                            <p className = "indent-5 text-xl">{favoriteGameLog?.start_date}</p>
                                                        </>
                                                    )}
                                                    {favoriteGameLog?.completion_date && (
                                                        <>
                                                            <h1 className = "text-2xl font-main-title">Completion Date:</h1>
                                                            <p className = "indent-5 text-xl">{favoriteGameLog?.completion_date}</p>
                                                        </>
                                                    )}
                                                    <h1 className = "text-2xl font-main-title">100% Completion:</h1>
                                                    <p className = "indent-5 text-xl">{favoriteGameLog?.full_completion ? "Yes" : "No"}</p>
                                                </div>
                                            </div>
                                        </div>
                                    </Link>
                                </RandomColor>
                                <p className = "break-up-line mb-10"></p>
                            </>
                        )}
                        <SectionHeader title = "Favorites" />
                        <div className = "grid grid-cols-2 gap-6 indent-5">
                            <div className = "space-y-2">
                                <div className = "space-y-2 pr-4 border-r border-white">
                                    <RandomColor constant><h1 className = "text-xl font-main-title">Developer(s):</h1></RandomColor>
                                    <p className = "break-up-line indent-10"> {profile.statistics?.favorite_developers?.length ? profile.statistics.favorite_developers.map(x => x.label).join(", ") : "No favorite developers..."}</p>
                                    <RandomColor constant><h1 className = "text-xl font-main-title">Publisher(s):</h1></RandomColor>
                                    <p className = "break-up-line indent-10"> {profile.statistics?.favorite_publishers?.length ? profile.statistics.favorite_publishers.map(x => x.label).join(", ") : "No favorite publishers..."}</p>
                                    <RandomColor constant><h1 className = "text-xl font-main-title">Genre(s):</h1></RandomColor>
                                    <p className = "break-up-line indent-10"> {profile.statistics?.favorite_genres?.length ? profile.statistics.favorite_genres.map(x => x.label).join(", ") : "No favorite genres..."}</p>
                                </div>
                            </div>
                            <div className = "space-y-2 mb-10">
                                <RandomColor constant><h1 className = "text-xl font-main-title">Platform(s):</h1></RandomColor>
                                <p className = "break-up-line indent-10"> {profile.statistics?.favorite_platforms?.length ? profile.statistics.favorite_platforms.map(x => x.label).join(", ") : "No favorite platforms..."}</p>
                                <RandomColor constant><h1 className = "text-xl font-main-title">Franchise(s):</h1></RandomColor>
                                <p className = "break-up-line indent-10"> {profile.statistics?.favorite_franchises?.length ? profile.statistics.favorite_franchises.map(x => x.label).join(", ") : "No favorite franchises..."}</p>
                                <RandomColor constant><h1 className = "text-xl font-main-title">Series:</h1></RandomColor>
                                <p className = "break-up-line indent-10"> {profile.statistics?.favorite_series?.length ? profile.statistics.favorite_series.map(x => x.label).join(", ") : "No favorite series..."}</p>
                            </div>
                        </div>
                    </div>
                </div>
                {profile.statistics && (
                    <>
                        <SectionHeader title = "Statistics" />
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-5 mb-5">
                            <StatCard title = "Total Games" value = {profile.statistics!.total_games} />
                            <StatCard title = "Total Completed Games" value = {profile.statistics!.completed_games} />
                            <StatCard title = "Completion Rate" value = {`${completionRate}%`} />
                            <StatCard title = "Total Playtime" value = {`${profile.statistics!.total_playtime} Hours`} />
                        </div>
                        <div className = "bg-ui p-4 rounded-lg outline-4 outline-white mb-5">
                            <RandomColor constant><h1 className = "text-xl font-main-title mb-2">Genre Variety</h1></RandomColor>
                            {profile.statistics.genre_variety.index === 0 ? (
                                <DataNotAvailable text = "Add games to calculate genre variety data!" />
                            ) : (
                                <>
                                    <p>Score Index: {profile.statistics.genre_variety.index.toFixed(2)}</p>
                                    <div className = "w-full bg-black h-3 rounded mt-2">
                                        <div className="h-3 bg-blue-500 rounded"
                                        style = {{width: `${Math.min(profile.statistics.genre_variety.index * 100, 100)}%`,}} />
                                    </div>
                                </>
                            )}
                        </div>
                        <div className = "grid grid-cols-1 lg:grid-cols-2 gap-10 mb-5">
                            <div>
                                <RandomColor constant><h1 className = "text-xl font-main-title mb-2">Overall Game Status</h1></RandomColor>
                                {(profile.statistics.completed_games === 0 && profile.statistics.paused_games === 0 && profile.statistics.playing_games === 0 && profile.statistics.backlog_games === 0 && profile.statistics.dropped_games === 0) ? (
                                    <DataNotAvailable text = "Add games to calculate game status data!" />
                                ) : (
                                    <ResponsiveContainer width = "100%" height = {300}>
                                        <PieChart>
                                            <Pie data = {[{name: "Completed", value: profile.statistics!.completed_games}, {name: "Playing", value: profile.statistics!.playing_games}, {name: "Backlog", value: profile.statistics!.backlog_games}, {name: "Dropped", value: profile.statistics!.dropped_games}, {name: "Paused", value: profile.statistics!.paused_games},]} dataKey = "value" nameKey = "name" outerRadius = {125}>
                                                {statusData.map((_, index) => (<Cell key = {`cell-${index}`} fill = {statisticColors[index % statisticColors.length]} />))}
                                            </Pie>
                                            <Tooltip content = {<CustomTooltip />} />
                                        </PieChart>
                                    </ResponsiveContainer>
                                )}
                            </div>
                            <div>
                                <RandomColor constant><h1 className = "text-xl font-main-title mb-2">Games Completed Per Year</h1></RandomColor>
                                {profile.statistics.yearly_completed_games.length === 0 ? (
                                    <DataNotAvailable text = "Add games to calculate game completion data!" />
                                ) : (
                                    <ResponsiveContainer width = "100%" height = {300}>
                                        <BarChart data = {lastFiveYears}>
                                            <CartesianGrid strokeDasharray = "3 3" />
                                            <XAxis dataKey = "year" />
                                            <YAxis allowDecimals = {false} />
                                            <Tooltip content = {<CustomTooltip />} />
                                            <Bar dataKey = "count" fill = "#65DD65" radius = {[6, 6, 0, 0]} />
                                        </BarChart>
                                    </ResponsiveContainer>
                                )}
                            </div>
                        </div>
                        <div className = "grid grid-cols-1 lg:grid-cols-2 gap-10 mb-5">
                            <div>
                                <RandomColor constant><h1 className = "text-xl font-main-title">Commitment Chart</h1></RandomColor>
                                <p className = "indent-5">Average playtime per game!</p>
                                {commitmentData.length === 0 ? (
                                    <DataNotAvailable text = "Add games to calculate commitment data!" />
                                ) : (
                                    <ResponsiveContainer width = "100%" height = {300}>
                                        <BarChart data = {commitmentData}>
                                            <XAxis dataKey = "label" />
                                            <YAxis allowDecimals = {false} />
                                            <Tooltip content = {<CustomTooltip />} />
                                            <Bar dataKey = "count" stroke = {commitmentColor} fill = {commitmentColor} radius = {[6, 6, 0, 0]} />
                                        </BarChart>
                                    </ResponsiveContainer>
                                )}
                            </div>
                            <div>
                                <RandomColor constant><h1 className = "text-xl font-main-title mb-2">Playstyle Type: {profile.statistics.playstyle.primary.replace("_", " ")}</h1></RandomColor>
                                {playstyleRadarData.length === 0 ? (
                                    <DataNotAvailable text = "Add games to calculate playstyle data!" />
                                ) : (
                                    <ResponsiveContainer width = "100%" height = {300}>
                                        <RadarChart data = {playstyleRadarData}>
                                            <PolarGrid />
                                            <PolarAngleAxis dataKey = "metric" />
                                            <Radar dataKey = "value" stroke = {radarColor} fill = {radarColor} fillOpacity = {0.6} />
                                            <Tooltip content = {<CustomTooltip />} />
                                        </RadarChart>
                                    </ResponsiveContainer>
                                )}
                            </div>
                        </div>
                        <div>
                            <RandomColor constant><h1 className = "text-xl font-main-title mb-2">Games Timeline (Past Year)</h1></RandomColor>
                            {(timelineData.length === 0) ? (
                                <DataNotAvailable text = "No games completed within past year!" />
                            ) : (
                                <ResponsiveContainer width = "100%" height = {300}>
                                    <LineChart margin = {{top: 20, right: 20, bottom: 20, left: 20}}>
                                        <CartesianGrid />
                                        <XAxis type = "number" dataKey = "x" domain = {[oneYearAgo.getTime(), now.getTime()]} tickFormatter = {(time) => new Date(time).toLocaleDateString()} />
                                        <YAxis type="number" dataKey="y" name = "Hours Played" />
                                        <Tooltip
                                            cursor = {{strokeDasharray: '3 3'}}
                                            content = {({active, payload}) => {
                                                if (active && payload && payload.length) {
                                                    const point = payload[0].payload;
                                                    const {gameTitle, start, end, y} = point;
                                                    const startDate = new Date(start).toLocaleDateString();
                                                    const endDate = end ? new Date(end).toLocaleDateString() : "Ongoing";
                                                    return (
                                                        <div className = "bg-ui p-2 rounded-lg outline-4 outline-white shadow-md">
                                                            <p className = "font-main-title">{gameTitle}</p>
                                                            <p>Playtime: {y}</p>
                                                            <p>Start: {startDate}</p>
                                                            <p>End: {endDate}</p>
                                                        </div>
                                                    );
                                                }
                                                return null;
                                            }}
                                        />
                                        {timelineData.map((log, index) => {
                                            const color = statisticColors[index % statisticColors.length];
                                            const points = log.end ? [{x: log.start, y: log.y, gameTitle: log.gameTitle, start: log.start, end: log.end}, {x: log.end, y: log.y, gameTitle: log.gameTitle, start: log.start, end: log.end},] : [{x: log.start, y: log.y, gameTitle: log.gameTitle, start: log.start, end: log.end}];
                                            return (<Line key = {`line-${index}`} type = "linear" data = {points} dataKey = "y" stroke = {color} strokeWidth = {2} dot = {{r: 4}} activeDot = {{r: 6}}></Line>);
                                        })}
                                    </LineChart>
                                </ResponsiveContainer>
                            )}
                        </div>
                        <div className = "bg-ui p-4 rounded-lg outline-4 outline-white mb-5">
                            <RandomColor constant><h1 className = "text-xl font-main-title mb-2">Drop-Off Depth</h1></RandomColor>
                            {profile.statistics.dropoff_depth === 0 ? (
                                <DataNotAvailable text = "Add games to calculate drop-off data!" />
                            ) : (
                                <>
                                    <p className = "text-2xl">{profile.statistics.dropoff_depth.toFixed(1)} Hours</p>
                                    <p className = "text-xl opacity-80 mt-1">Average playtime before dropping a game!</p>
                                    <div className = "w-full bg-black h-3 rounded mt-3">
                                        <div className = "h-3 bg-blue-500 rounded" style = {{width: `${Math.min(profile.statistics.dropoff_depth / 40, 1) * 100}%`,}} />
                                    </div>
                                </>
                            )}
                            <p className="text-xl mt-1 opacity-70">Lower = Quicker Drop | Higher = More Commitment</p>
                        </div>
                    </>
                )}
            </div>
        );
    }
};

export default Profile;