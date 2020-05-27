import {Entity, PrimaryGeneratedColumn, Column} from "typeorm";

@Entity()
export class Message {

    @PrimaryGeneratedColumn()
    id: number;

    @Column()
    NAME: string;

    @Column()
    MESSAGE: string;

    @Column()
    DATE: string;

    @Column()
    TIME: string;

}
